from picamera.array import PiRGBArray

from picamera import PiCamera

from gpiozero import LED

from gpiozero import Button

import time

import datetime

import numpy as np

import cv2

# initialize the camera and grab a reference to the raw camera capture

camera = PiCamera()

camera.resolution = (640, 480)

camera.framerate = 32

camera.rotation = 180



reset = Button(4, pull_up = True)

flag = LED(15)#black

result = LED(18)#red





humanDetected = False

#deux output : flag pour dire quand un résulat est envoyé et le résultat pour dire si un humain est détecté

flag.off()

result.off()





while True:

    if reset.is_pressed: #lecture du flag envoyé par l'arduino

        print("outofOPENCV")

    else:

        print("buttonpressed")

        rawCapture = PiRGBArray(camera, size=(640, 480))

        # allow the camera to warmup

        time.sleep(0.1)

        hog = cv2.HOGDescriptor()

        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # capture frames from the camera

        i = 0

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            i +=1

            image = frame.array

            humanDetected = False



            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            boxes, weights = hog.detectMultiScale(image, winStride=(8,8) )

            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            for (xA, yA, xB, yB) in boxes:

                # display the detected boxes in the colour picture

                cv2.rectangle(image, (xA, yA), (xB, yB),(0, 255, 0), 2)

                

                humanDetected = True

            cv2.imshow("Frame", image);

            

            if humanDetected:

                print("Human Detected, flag ON")

                result.on()

                

                flag.on()

                now = datetime.datetime.now()

                formatNow = now.strftime("%Y-%m-%d_%H-%M-%S")

                filename = f"humanDetected_{formatNow}.jpg"

                cv2.imwrite(filename, image)

                time.sleep(10)

                result.off()

                

                flag.off()

                print("flag OFF")

                break

            

            if i == 6:

                

                result.off()

                flag.on()

                print("no human detected, flag on")

                time.sleep(10)

                flag.off()

                print("flag off")

                break

            key = cv2.waitKey(1) & 0xFF

            rawCapture.truncate(0)

            if key == ord("q"):

               break