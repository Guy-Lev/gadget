from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import distinct
db = SQLAlchemy()

### Add models here

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def to_dict(self):
        return  {'id': self.id, 'type': 'user', 'attributes':{'name':self.name, 'description':self.description}}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def get_attibute_dict(self):
        return {'email': self.email, 'name': self.name}

    def get_relationship_dict(self):
        return {'roles':{'data':[{'id':r.id, 'type':'role'} for r in self.roles]}}

    def to_dict(self):
        return  {'id': self.id, 'type': 'user', 'attributes': self.get_attibute_dict(), 'relationships': self.get_relationship_dict()}


class Investigation(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    created_by_id = db.Column(db.Integer, db.ForeignKey
                              ('user.id', ondelete='CASCADE'), index=True)
    created_by = db.relationship("User")
    name = db.Column(db.String(255))
    log_url = db.Column(db.String(511))
    ready = db.Column(db.Boolean, default=False)
    error = db.Column(db.String)
    events = db.relationship("Event", backref="investigation")
    event_types = db.relationship("EventType", backref="investigation")

    def get_attibute_dict(self):
        return {
            'name': self.name,
            'created-at': self.created_at.isoformat() + 'Z',
            'created-by': self.created_by.id if self.created_by else None, #TODO get out attr
            'log-url': self.log_url,
            'error': self.error,
            'ready': self.ready,
        }

    def get_relationship_dict(self, extended):
        relationships = {}
        if extended:
            relationships = {
#                'entities': {'data':[{'id':e.id, 'type':'entity'} for e in self.entities]},
                'events': {'data':[{'id':e.id, 'type':'event'} for e in self.events]},
                'event-types':{'data':[{'id':e.id, 'type':'event-type'} for e in self.event_types]}}
        if self.created_by:
            relationships['created-by'] = {'data':{'id': self.created_by.id, 'type':'user'}}
        return relationships

    def to_dict(self, extended=True):
        return {'attributes': self.get_attibute_dict(),'relationships':self.get_relationship_dict(extended), 'id': self.id, 'type':'investigations'}


entity_event = db.Table('entity_event',
                        db.Column('entity_id', db.Integer(), db.ForeignKey(
                            'entity.id', ondelete='CASCADE')),
                        db.Column('event_id', db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE')))


class Entity(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    str_id = db.Column(db.String(255))
    events = db.relationship('Event', secondary=entity_event,
                             backref=db.backref('entity', lazy='dynamic'))
    is_selected = db.Column(db.Boolean, default=False)

    def get_attibute_dict(self):
        return {
            #'investigation': self.investigation_id,
            'str-id': self.str_id,
            'is-selected': self.is_selected
        }

    def get_relationship_dict(self):
        return {'events':{'data':[{'id':e.id, 'type':'event'} for e in self.events]}}

    def to_dict(self):
        return {'attributes': self.get_attibute_dict(), 'relationships':self.get_relationship_dict(), 'id': self.id, 'type':'entity'}


class Event(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    investigation_id = db.Column(db.Integer, db.ForeignKey('investigation.id',  ondelete='CASCADE'), index=True, nullable=False)
    name = db.Column(db.String(255))
    state = db.Column(db.String(128))
    update = db.Column(JSONB)
    timeStamp = db.Column(db.DateTime(), index=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id', ondelete='CASCADE'))
    event_type = db.relationship("EventType")

    params = db.Column(JSONB)
    entities = db.relationship('Entity', secondary=entity_event,
                               backref=db.backref('event', lazy='dynamic'))

    def get_relationship_dict(self):
        return{
            'event-type': {'data':{'id':self.event_type_id, 'type':'event-type'}},
        }

    def get_attibute_dict(self):
        return {
            'investigation': self.investigation_id,
            'name': self.name,
            'state': self.state,
            'update': self.update,
            'time-stamp': self.timeStamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'params':self.params,
            'entities':[e.id for e in self.entities],
        }

    def to_dict(self):
        return {'attributes': self.get_attibute_dict(),'relationships':self.get_relationship_dict(), 'id': self.id, 'type':'event'}


class EventType(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    investigation_id = db.Column(db.Integer, db.ForeignKey('investigation.id', ondelete='CASCADE'), index=True)
    name = db.Column(db.String)
    is_selected = db.Column(db.Boolean, default=False)

    def get_attibute_dict(self):
        return {
            'name': self.name,
            'investigation': self.investigation_id,
            'is-selected': self.is_selected
        }

    def to_dict(self):
        return {'attributes': self.get_attibute_dict(), 'id': self.id, 'type':'event_type'}
