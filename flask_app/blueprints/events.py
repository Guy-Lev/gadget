import http
from flask import Blueprint, jsonify, request
from ..models import Event, db
events = Blueprint("events", __name__, template_folder="templates")

@events.route('', methods=['GET'])
def get_all():
    event_models = db.session.query(Event)
    events =  [event.to_dict() for event in event_models]
    return jsonify({'data': events})


@events.route('/<int:event_id>', methods=['GET'])
def get(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()
    if not event:
        return "No such event", http.client.NOT_FOUND
    return jsonify({'data': event.to_dict()})
