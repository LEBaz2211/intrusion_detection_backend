from app import db
from datetime import datetime

class IntrusionEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    event_type = db.Column(db.String(50))
    details = db.Column(db.Text)
    status = db.Column(db.String(20), default='new')

    def __repr__(self):
        return f'<IntrusionEvent {self.id}>'


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    device_type = db.Column(db.String(50))
    last_check_in = db.Column(db.DateTime)
    battery_level = db.Column(db.Float)

    intrusion_events = db.relationship('IntrusionEvent', backref='device', lazy=True)

    def __repr__(self):
        return f'<Device {self.id}>'


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    address = db.Column(db.String(200))

    devices = db.relationship('Device', backref='location', lazy=True)

    def __repr__(self):
        return f'<Location {self.id}>'


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    log_level = db.Column(db.String(10))
    message = db.Column(db.Text)

    def __repr__(self):
        return f'<Log {self.id}>'