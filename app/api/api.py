from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/events/recent', methods=['GET'])
def get_recent_events():
    # Logic to fetch recent events
    return jsonify([])

@api.route('/events', methods=['GET'])
def get_events_by_date():
    # Logic to fetch events by date
    return jsonify([])

@api.route('/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    # Logic to fetch specific event details
    return jsonify({})
