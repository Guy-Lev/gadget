from __future__ import absolute_import

import functools
import os
import sys
import munch
import gadget

import logging
import logging.handlers
import logbook
import urllib.request
import requests

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from celery.log import redirect_stdouts_to_logger
from sqlalchemy import and_
from .app import create_app
from .models import Investigation, Event, Entity, EventType, db

logger = logbook.Logger(__name__)

TYPE_CODES = munch.Munch(
    CREATE='CR',
    OPERATION='OP',
    STATE='ST',
    UPDATE='UP',
    ERROR='ER',
)

queue = Celery('tasks', broker='redis://localhost')
queue.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
)

def setup_log(**args):
    logbook.SyslogHandler().push_application()
    logbook.StreamHandler(sys.stderr, bubble=True).push_application()
    redirect_stdouts_to_logger(args['logger']) # logs to local syslog
    if os.path.exists('/dev/log'):
        h = logging.handlers.SysLogHandler('/dev/log')
    else:
        h = logging.handlers.SysLogHandler()
    h.setLevel(args['loglevel'])
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    h.setFormatter(formatter)
    args['logger'].addHandler(h)

APP = None

def needs_app_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        global APP

        if APP is None:
            APP = create_app()

        with APP.app_context():
            return f(*args, **kwargs)

    return wrapper

@queue.task
@needs_app_context
def process_log(log_url, investigation_id):
    investigation = db.session.query(Investigation).filter_by(id=investigation_id).one()
    try:
        r = requests.get(log_url)
        for line in r.content.splitlines():
            log_line = gadget.parse_log_line(line.decode('UTF8'))
            if not log_line:
                continue
            elif log_line.type == TYPE_CODES.OPERATION:
                _handle_operation_event(log_line, investigation)
            elif  log_line.type == TYPE_CODES.STATE:
                _handle_state_event(log_line, investigation)
            elif log_line.type == TYPE_CODES.UPDATE:
                _handle_update_event(log_line, investigation)
            elif log_line.type == TYPE_CODES.ERROR:
                _handle_error_event(log_line, investigation)
            elif log_line.type == TYPE_CODES.CREATE:
                _handle_creation_event(log_line, investigation)
    except Exception as e:
        investigation.error = str(e)

    investigation.ready = True
    db.session.commit()

def _create_basic_event(log_line, investigation):
    event = Event()
    event.timeStamp = log_line.timestamp
    event.params = log_line.params
    event.investigation = investigation
    return event


def _get_or_create_event_type(name, investigation):
    event_type = db.session.query(EventType).filter_by(name=name, investigation_id=investigation.id).first()
    if not event_type:
        event_type = EventType()
        event_type.name = name
        event_type.investigation = investigation
        db.session.add(event_type)
    return event_type

def _handle_operation_event(log_line, investigation):
    entities = []
    for str_id in log_line.entities:
        entity = db.session.query(Entity).join(Entity.events).filter(and_(Entity.str_id==str_id, Event.investigation_id==investigation.id)).first()
        if not entity:
            entity = Entity()
            entity.str_id = str_id
            db.session.add(entity)
        entities.append(entity)
    event = _create_basic_event(log_line, investigation)
    event.event_type =  _get_or_create_event_type("operation", investigation)
    event.name = log_line.name
    event.entities = entities
    db.session.add(event)

def _handle_state_event(log_line, investigation):
    entity = db.session.query(Entity).join(Entity.events).filter(and_(Entity.str_id==log_line.entity, Event.investigation_id==investigation.id)).first()
    if not entity:
        entity = Entity()
        entity.str_id = log_line.entity
        db.session.add(entity)
    event = _create_basic_event(log_line, investigation)
    event.event_type = _get_or_create_event_type("state", investigation)
    event.state = log_line.state
    event.entities = [entity]
    db.session.add(event)

def _handle_update_event(log_line, investigation):
    entity = db.session.query(Entity).join(Entity.events).filter(and_(Entity.str_id==log_line.entity, Event.investigation_id==investigation.id)).first()
    if not entity:
        entity = Entity()
        entity.str_id = log_line.entity
        db.session.add(entity)

    event = _create_basic_event(log_line, investigation)
    event.event_type = _get_or_create_event_type("update", investigation)
    event.update = log_line.update
    event.entities = [entity]
    event.investigation_id = investigation.id
    db.session.add(event)

def _handle_error_event(log_line, investigation):
    event = _create_basic_event(log_line, investigation)
    event.event_type = _get_or_create_event_type("error", investigation)
    event.event_type.is_selected = True
    event.params = log_line.params
    db.session.add(event)

def _handle_creation_event(log_line, investigation):
    entity = db.session.query(Entity).join(Entity.events).filter(and_(Entity.str_id==log_line.entity, Event.investigation_id==investigation.id)).first()
    if entity:
        warn_msg = "Creation of the entity \"" + log_line.entity + "\" happened more than once."
        if not investigation.warning:
            investigation.warning = warn_msg
        elif warn_msg not in investigation.warning:
            investigation.warning = investigation.warning.join(warn_msg)
    else:
        entity = Entity()
        entity.str_id = log_line.entity
        db.session.add(entity)

    event = _create_basic_event(log_line, investigation)
    event.event_type = _get_or_create_event_type("creation", investigation)
    event.entities = [entity]
    event.investigation_id = investigation.id
    db.session.add(event)

after_setup_logger.connect(setup_log)
after_setup_task_logger.connect(setup_log)
