#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <Wire.h>
#include <math.h>
#include <sam.h>

// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
#define LASER_PIN 5
#define ALERT_PIN 10
#define FLAG_PIN A3
#define RESULT_PIN A4

#define PROJECT_DEVICE_ID 01
// Used for hardware & software SPI
#define LIS3DH_CS 10

// FSM states
enum STATE {
  MONITORING,
  AWAITING_ANALYSIS,
};
STATE state = MONITORING;

unsigned long monitoring_elapsed_time;
unsigned long triggered_elapsed_time;
unsigned long emission_elapsed_time;
unsigned long raspberry_elapsed_time;
const int heartbeat_frequency = 1000 * 60;   //in milliseconds
const int emission_cooldown = 1000 * 10;     //in milliseconds
const int triggered_cooldown = 1000 * 10;    //in milliseconds
const int raspberry_timeout = 1000 * 15;


// TTN Configuration
static const u1_t PROGMEM APPEUI[8] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void os_getArtEui(u1_t* buf) {
  memcpy_P(buf, APPEUI, 8);
}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8] = { 0xAD, 0x2C, 0x06, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
void os_getDevEui(u1_t* buf) {
  memcpy_P(buf, DEVEUI, 8);
}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from the TTN console can be copied as-is.
static const u1_t PROGMEM APPKEY[16] = { 0xD2, 0x63, 0x6B, 0xC4, 0x9A, 0xCB, 0x13, 0x81, 0x75, 0x02, 0x75, 0x73, 0x73, 0xB4, 0x4B, 0x45 };
void os_getDevKey(u1_t* buf) {
  memcpy_P(buf, APPKEY, 16);
}

// payload to send to TTN gateway
static uint8_t payload[64];
static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 7;

// Pin mapping for Adafruit Feather M0 LoRa
const lmic_pinmap lmic_pins = {
  .nss = 8,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 4,
  .dio = { 3, 6, LMIC_UNUSED_PIN },
  .rxtx_rx_active = 0,
  .rssi_cal = 8,  // LBT cal for the Adafruit Feather M0 LoRa, in dB
  .spi_freq = 8000000,
};

void setup() {
  pinMode(RESULT_PIN, INPUT);
  pinMode(LASER_PIN, INPUT);
  pinMode(ALERT_PIN, OUTPUT);
  digitalWrite(ALERT_PIN, LOW);
  attachInterrupt(digitalPinToInterrupt(LASER_PIN), detection, RISING);
  //while (!Serial);
  Serial.begin(115200);

  // LMIC init.
  os_init();
  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();
  // Disable link-check mode and ADR, because ADR tends to complicate testing.
  LMIC_setLinkCheckMode(0);
  // Set the data rate to Spreading Factor 7.  This is the fastest supported rate for 125 kHz channels, and it
  // minimizes air time and battery power. Set the transmission power to 14 dBi (25 mW).
  LMIC_setDrTxpow(DR_SF7, 14);
  // Start job (sending automatically starts OTAA too)
  do_send(&sendjob);
}

void loop() {
  // we call the LMIC's runloop processor. This will cause things to happen based on events and time. One
  // of the things that will happen is callbacks for transmission complete or received messages. We also
  // use this loop to queue periodic data transmissions.  You can put other things here in the loop() routine,
  // but beware that LoRaWAN timing is pretty tight, so if you do more than a few milliseconds of work, you
  // will want to call os_runloop_once() every so often, to keep the radio running.
  os_runloop_once();
  //Serial.println(digitalRead(LASER_PIN));

  switch (state) {

    case MONITORING:  //Emits heartbeats. Any laser break will raise an interruption.
      if (millis() - monitoring_elapsed_time > heartbeat_frequency) {
        if (!digitalRead(LASER_PIN)) {
          emitMessage("ACTIVE");
        } else {
          emitMessage("INACTIVE");
        }
        monitoring_elapsed_time = millis();
      }
      break;

    case AWAITING_ANALYSIS:
      if (millis() - raspberry_elapsed_time < raspberry_timeout) {

        //Serial.print("FLAG:");
        //Serial.println(analogRead(FLAG_PIN));
        if (analogRead(FLAG_PIN) > 500) {  // PIN 11

          //Serial.print("RESULT:");
          //Serial.println(analogRead(RESULT_PIN));
          if (analogRead(RESULT_PIN) > 500) {  // PIN 12
            emitMessage("INTRUDER_DETECTED");
            digitalWrite(ALERT_PIN, LOW);
            state = MONITORING;
          } else {
            Serial.println("FALSE_POSITIVE.");
            digitalWrite(ALERT_PIN, LOW);
            state = MONITORING;
          }
        }

      } else if (millis() - raspberry_elapsed_time >= raspberry_timeout) {
        Serial.println("RASPBERRY TIMEOUT.");
        emitMessage("RASPBERRY_TIMEOUT");
        digitalWrite(ALERT_PIN, LOW);
        state = MONITORING;
      }
      break;
  }
}

void detection() {
  Serial.println("DETECTION!");
  if (state == MONITORING) {
    digitalWrite(ALERT_PIN, 100);
    Serial.println("LASER TRIGGERED! AWAITING ANALYSIS.");
    state = AWAITING_ANALYSIS;
    raspberry_elapsed_time = millis();
  }
}

void emitMessage(String messageString) {
  String message = "device_id:" + String(PROJECT_DEVICE_ID) + ", power:" + "100%" + ", status:" + messageString;

  if (millis() - emission_elapsed_time > emission_cooldown) {
    Serial.print("Sending message... ");
    Serial.println(message);

    message.getBytes(payload, 60);

    LMIC.frame[0] = 1;  // Port 1 is used
    // Buffer
    memcpy(LMIC.frame + 1, payload, sizeof(payload));
    // Send message
    LMIC_setTxData2(1, LMIC.frame, sizeof(payload) + 1, 0);
    memset(payload, 0, sizeof(payload));

    emission_elapsed_time = millis();
  } else {
    Serial.println("Emission cooldown! Message:" + message);
  }
}

void onEvent(ev_t ev) {
  switch (ev) {
    case EV_SCAN_TIMEOUT:
      Serial.println(F("EV_SCAN_TIMEOUT"));
      break;
    case EV_BEACON_FOUND:
      Serial.println(F("EV_BEACON_FOUND"));
      break;
    case EV_BEACON_MISSED:
      Serial.println(F("EV_BEACON_MISSED"));
      break;
    case EV_BEACON_TRACKED:
      Serial.println(F("EV_BEACON_TRACKED"));
      break;
    case EV_JOINING:
      Serial.println(F("EV_JOINING"));
      break;
    case EV_JOINED:
      Serial.println(F("EV_JOINED"));
      LMIC_setLinkCheckMode(0);
      break;
    case EV_JOIN_FAILED:
      Serial.println(F("EV_JOIN_FAILED"));
      break;
    case EV_REJOIN_FAILED:
      Serial.println(F("EV_REJOIN_FAILED"));
      break;
    case EV_TXCOMPLETE:
      Serial.println(F("Payload sent successfully"));
      // Schedule next transmission
      //os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
      break;
    case EV_LOST_TSYNC:
      Serial.println(F("EV_LOST_TSYNC"));
      break;
    case EV_RESET:
      Serial.println(F("EV_RESET"));
      break;
    case EV_RXCOMPLETE:
      // data received in ping slot
      Serial.println(F("EV_RXCOMPLETE"));
      break;
    case EV_LINK_DEAD:
      Serial.println(F("EV_LINK_DEAD"));
      break;
    case EV_LINK_ALIVE:
      Serial.println(F("EV_LINK_ALIVE"));
      break;
    case EV_TXSTART:
      Serial.println(F("Starting new transmission"));
      break;
    case 20:
      Serial.println("ERROR: Unknown event 20");
      Serial.println("Restarting Arduino...");
      NVIC_SystemReset();  // Microcontroller reset
    default:
      Serial.print(F("ERROR: Unknown event "));
      Serial.println(ev);
      break;
  }
}

void do_send(osjob_t* j) {
  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {
    // prepare upstream data transmission at the next possible time.
    // transmit on port 1 (the first parameter); you can use any value from 1 to 223 (others are reserved).
    // don't request an ack (the last parameter, if not zero, requests an ack from the network).
    // Remember, acks consume a lot of network resources; don't ask for an ack unless you really need it.
    LMIC_setTxData2(1, payload, sizeof(payload) - 1, 0);
  }
  // Next TX is scheduled after TX_COMPLETE event.
}