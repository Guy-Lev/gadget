import http
from flask import Blueprint, jsonify, request
from .utils import validate_schema
from ..models import EventType, db
event_types = Blueprint("event-types", __name__, template_folder="templates")


@event_types.route('/<int:event_type_id>', methods=['GET'])
def get(event_type_id):
    event_type = db.session.query(EventType).filter_by(id=event_type_id).first()
    if not event_type:
        return "No such event type", http.client.NOT_FOUND
    return jsonify({'data': event_type.to_dict()})


@event_types.route('/<int:event_type_id>', methods=['PATCH'])
@validate_schema({
    'type': 'object',
    "properties": {
        "data":{
        'type': 'object',
            "properties": {
                "attributes": {
                "is-selected": {'type': 'bool'},
                }
            }
        },
        "required": ["is_selected"]
    },
    "required": ["data"]
})
def update(event_type_id):
    event_type = db.session.query(EventType).filter_by(id=event_type_id).first()
    if not event_type:
        return "No such entity", http.client.NOT_FOUND
    event_type.is_selected = request.json['data']['attributes']['is-selected']
    db.session.commit()
    return jsonify({'data':event_type.to_dict()})
