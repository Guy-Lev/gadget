import http
from flask import Blueprint, jsonify, request
from .utils import validate_schema
from ..models import Entity, Event, db
entities = Blueprint("entities", __name__, template_folder="templates")

@entities.route('', methods=['GET'])
def get_all():
    investigation_id = request.args.get('investigation_id', None)
    if investigation_id:
        entity_models = db.session.query(Entity).join(Entity.events)\
                                                .filter(Event.investigation_id == investigation_id)
    else:
        entity_models = db.session.query(Entity)
    entities =  [entity.to_dict() for entity in entity_models]
    return jsonify({'data':entities})


@entities.route('/<int:entity_id>', methods=['GET'])
def get(entity_id):
    entity = db.session.query(Entity).filter_by(id=entity_id).first()
    if not entity:
        return "No such entity", http.client.NOT_FOUND
    return jsonify({'data':entity.to_dict()})



@entities.route('/<int:entity_id>', methods=['PATCH'])
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
def update(entity_id):
    entity = db.session.query(Entity).filter_by(id=entity_id).first()
    if not entity:
        return "No such entity", http.client.NOT_FOUND
    entity.is_selected = request.json['data']['attributes']['is-selected']
    db.session.commit()
    return jsonify({'data':entity.to_dict()})
