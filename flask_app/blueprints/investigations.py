import http
import flux
from .utils import validate_schema
from flask import Blueprint, jsonify, request, abort
from ..models import Investigation, Event, EventType, Entity, db
from ..tasks import process_log
from flask.ext.login import current_user
from sqlalchemy import or_, and_

investigations = Blueprint("investigations", __name__, template_folder="templates")


def get_filtered_events(investigation_id):
    filtered_events = db.session.query(Event).filter(Event.investigation_id == investigation_id)\
                                             .outerjoin(Event.entities)\
                                             .join(Event.event_type)\
                                             .filter(or_(EventType.is_selected == True,Entity.is_selected == True))\
                                             .group_by(Event.id).limit(50).all()
    return filtered_events

@investigations.route('', methods=['GET'])
def get():
    investigation_id = request.args.get('investigation_id', None)
    if investigation_id:
        return get_by_id(investigation_id)

    investigation_models = db.session.query(Investigation)
    investigation_list =  [investigation.to_dict(extended=False) for investigation in investigation_models]
    return jsonify({'data':investigation_list})


@investigations.route('/<int:investigation_id>', methods=['GET'])
def get_by_id(investigation_id):
    search_str = request.args.get('search', "")
    investigation = db.session.query(Investigation).filter_by(id=investigation_id).first()
    if not investigation:
        return "No such investigation", http.client.NOT_FOUND
    if search_str != "":
        filtered_entities = db.session.query(Entity).join(Entity.events).filter(and_(or_(Entity.is_selected == True,Entity.str_id.contains(search_str)),Event.investigation_id==int(investigation_id))).all()

        entities = filtered_entities
    else:
        entities =  db.session.query(Entity).join(Entity.events).filter(Event.investigation_id == investigation_id).all()

    events = get_filtered_events(investigation.id)
    ret = {'data':investigation.to_dict()}
    #TODO: Replace this hack with a query for only part of the entities and events
    ret['data']['relationships']['entities'] = {'data':[{'id':e.id, 'type':'entity'} for e in entities]}
    ret['data']['relationships']['events'] = {'data':[{'id':e.id, 'type':'event'} for e in events]}
    return jsonify(ret)


@investigations.route('', methods=['POST'])
@validate_schema({
    'type': 'object',
    "properties": {
        "data":{
            'type': 'object',
            "properties": {
                "attributes": {
                    "log_url": {'type': 'string'},
                    "name": {'type': 'string'},
                }
            }
        },
        "required": ["log_url", "name"]
    },
    "required": ["data"]
})
def create():
    investigation_json = request.json['data']['attributes']
    investigation = Investigation(
        name=investigation_json.get('name'),
        created_at=flux.current_timeline.datetime.utcnow(),
        created_by=current_user,
        log_url=investigation_json.get('log-url')
    )


    db.session.add(investigation)
    db.session.expire_on_commit = False
    db.session.commit()
    log_url = investigation_json.get('log-url')
    process_log.delay(log_url, investigation.id)
    #process_log(log_url, investigation.id)
    return jsonify({'data':investigation.to_dict()})


@investigations.route('/<int:investigation_id>', methods=['DELETE'])
def delete_investigation(investigation_id):
    investigation = db.session.query(Investigation).filter_by(id=investigation_id).first()
    if not investigation:
        abort(http.client.NOT_FOUND)

    db.session.query(Event).filter_by(investigation_id=investigation.id).delete()
    db.session.delete(investigation)
    db.session.commit()
    return jsonify({'data':investigation.to_dict()})
