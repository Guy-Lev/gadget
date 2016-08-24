import http
from flask import Blueprint, jsonify, request
from ..models import Entity, db
entities = Blueprint("entitiess", __name__, template_folder="templates")

@entities.route('', methods=['GET'])
def get_all():
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
def update(entity_id):
    entity = db.session.query(Entity).filter_by(id=entity_id).first()
    if not entity:
        return "No such entity", http.client.NOT_FOUND
    entity.is_selected = request.json['data']['attributes']['is-selected']
    db.session.commit()
    return jsonify({'data':entity.to_dict()})
