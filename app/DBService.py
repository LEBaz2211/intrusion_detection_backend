import sqlite3
import json
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
            name TEXT,
            status TEXT,
            x1 REAL,
            y1 REAL,
            x2 REAL,
            y2 REAL
        );
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS event_log (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            timestamp DATETIME,
            event_type TEXT,
            event_description JSON,
            FOREIGN KEY (device_id) REFERENCES devices(device_id)
        );
        ''')
        conn.close()

    def log_event(self, device_id, event_type, date,  description):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO event_log (device_id, timestamp, event_type, event_description) VALUES (?, ?, ?, ?)",
                     (device_id, date, event_type, description))
        conn.commit()
        conn.close()

    def add_device(self, device_id, name, status, x1, y1, x2, y2):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("INSERT INTO devices (device_id, name, status, x1, y1, x2, y2) VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (device_id, name, status, x1, y1, x2, y2))
            conn.commit()
        except sqlite3.IntegrityError:
            return json.dumps({"status": False})  # Device already exists
        finally:
            conn.close()
        return json.dumps({"status": True})

    def _dict_factory(self, cursor, row):
        """Converts database row objects to a dictionary."""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_device(self, device_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        cursor = conn.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
        device = cursor.fetchone()
        conn.close()
        return device if device else {}

    def get_devices(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        cursor = conn.execute("SELECT * FROM devices")
        devices = cursor.fetchall()
        conn.close()
        return devices

    def get_event_logs(self, device_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        cursor = conn.execute("SELECT * FROM event_log WHERE device_id = ?", (device_id,))
        log = cursor.fetchall()
        conn.close()
        return log
    
    def get_latest_event_log_id(self, device_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT MAX(event_id) FROM event_log WHERE device_id = ?", (device_id,))
        log = cursor.fetchone()
        conn.close()
        return log[0]
    
    def get_latest_event_log_status(self, device_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT MAX(event_type) FROM event_log WHERE device_id = ?", (device_id,))
        log = cursor.fetchone()
        conn.close()
        return log[0]
    
    def get_range_event_logs(self, device_id, number, start_id = None):
        if start_id is None:
            start_id = self.get_latest_event_log_id(device_id)  # Get the latest event log id
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        cursor = conn.execute("SELECT * FROM event_log WHERE device_id = ? AND event_id <= ? ORDER BY event_id DESC LIMIT ?", (device_id, start_id, number))
        log = cursor.fetchall()
        conn.close()
        return log


    def get_event_log_by_timestamp(self, timestamp):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        cursor = conn.execute("SELECT * FROM event_log WHERE timestamp = ?", (timestamp,))
        log = cursor.fetchall()
        conn.close()
        return log

    def get_event_log_by_timestamp(self, timestamp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM event_log WHERE timestamp = ?", (timestamp,))
        log = cursor.fetchall()
        conn.close()
        return log

    def update_device(self, device_id, name, status, x1, y1, x2, y2):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("UPDATE devices SET name = ?, status = ?, x1 = ?, y1 = ?, x2 = ?, y2 = ? WHERE device_id = ?",
                              (name, status, x1, y1, x2, y2, device_id))
        if cursor.rowcount == 0:
            return {"status": False} # Device not found


    def delete_device(self, device_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("DELETE FROM devices WHERE device_id = ?", (device_id,))
        if cursor.rowcount == 0:
            return json.dumps({"status": False})  # Device not found
        conn.commit()
        conn.close()
        return {"status": True}

if __name__ == "__main__":
    # Test the database service
    db_service = DatabaseService("app/database.db")
    db_service.add_device("test_device", "test_name", "test_status", 1, 2, 3, 4)
    print(db_service.get_device("test_device"))
    print(db_service.get_devices())
    now = datetime.now()
    db_service.log_event("test_device", "test_event", now, "test_description")
    print(db_service.get_event_logs("test_device"))
    print(db_service.get_event_log_by_timestamp(now))
    db_service.update_device("test_device", "test_name2", "test_status2", 5, 6, 7, 8)
    print(db_service.get_device("test_device"))
    print(db_service.get_range_event_logs("test_device", 10))
    db_service.delete_device("test_device")
    print(db_service.get_device("test_device"))
