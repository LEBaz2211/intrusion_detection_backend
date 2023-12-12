import sqlite3
from datetime import datetime

class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            model TEXT,
            location TEXT,
            installation_date DATE
        );
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS event_log (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            timestamp DATETIME,
            event_type TEXT,
            event_description TEXT,
            FOREIGN KEY (device_id) REFERENCES devices(device_id)
        );
        ''')
        conn.close()

    def log_event(self, device_id, event_type, description):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO event_log (device_id, timestamp, event_type, event_description) VALUES (?, ?, ?, ?)",
                     (device_id, datetime.now(), event_type, description))
        conn.commit()
        conn.close()

    def add_device(self, device_id, model, location, installation_date):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("INSERT INTO devices (device_id, model, location, installation_date) VALUES (?, ?, ?, ?)",
                         (device_id, model, location, installation_date))
            conn.commit()
        except sqlite3.IntegrityError:
            return False  # Device already exists
        finally:
            conn.close()
        return True

    def get_device(self, device_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
        device = cursor.fetchone()
        conn.close()
        return device

    def get_event_log(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM event_log")
        log = cursor.fetchall()
        conn.close()
        return log