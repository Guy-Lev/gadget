from flask import Blueprint, jsonify, request, abort
import re
import http.client
from itsdangerous import TimedSerializer, BadSignature
from apiclient.discovery import build
from httplib2 import Http
from oauth2client.client import OAuth2WebServerFlow
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.login import login_user, logout_user, current_user
from .models import Role, User, db

auth = Blueprint("auth", __name__, template_folder="templates")
client_id = "1013728488597-ilbto7lt5gl4vmt1lka5sm4uhkrd6a5v.apps.googleusercontent.com"
client_secret = "3Q_Jff1bh2ZoSoNCeEva5gc5"
_MAX_TOKEN_AGE = 60 * 60 * 24 * 365
_EMAIL = re.compile("^.*?@infinidat.com$")

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class InvalidEmail(Exception):
    pass


def _get_oauth2_identity(auth_code):

    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,

        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=request.host_url[:-1])

    credentials = flow.step2_exchange(auth_code)

    info = _get_user_info(credentials)
    return info


def _get_user_info(credentials):
    http_client = Http()
    if credentials.access_token_expired:
        credentials.refresh(http_client)
    credentials.authorize(http_client)
    service = build('oauth2', 'v2', http=http_client)
    return service.userinfo().get().execute()


def _get_token_serializer():
    return TimedSerializer(client_secret)


def is_email_valid(email):
    return _EMAIL.search(email) is not None


def get_or_create_user(email, name):
    if not is_email_valid(email):
        raise InvalidEmail()

    user = user_datastore.get_user(email)
    if not user:
        user = user_datastore.create_user(
            email=email,
            name=name)
        user_datastore.db.session.commit()
    else:
        if name is not None and name != user.name:
            user.name = name
            user_datastore.db.session.commit()

    return user


def _get_user_from_auth_token(auth_token):
    try:
        token_data = _get_token_serializer().loads(auth_token, max_age=_MAX_TOKEN_AGE)
    except BadSignature:
        abort(http.client.UNAUTHORIZED)

    return user_datastore.get_user(token_data['user_id'])


@auth.route("/restore", methods=['POST'])
def restore():
    user = _get_user_from_auth_token(request.json['auth_token'])
    if not user:
        abort(http.client.FORBIDDEN)

    assert user.id == request.json['id']
    login_user(user)
    return jsonify(request.json)


@auth.route("/login", methods=['POST'])
def login():
    auth_code = (request.json or {}).get('authorizationCode')
    if auth_code is None:
        abort(401)

    user_info = _get_oauth2_identity(auth_code)
    if not user_info:
        abort(401)

    user = get_or_create_user(user_info['email'], user_info['name'])
    token = _get_token_serializer().dumps({'user_id': user.id})
    login_user(user)

    return jsonify({
        'id': user.id,
        'auth_token': token,
        'user_info': user_info,
    })


@auth.route("/logout", methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()

    return ''


@auth.route("/reauth", methods=['POST'])
def reauth():
    token = (request.json or {}).get('auth_token')
    if token is None:
        abort(401)
    try:
        token_data = _get_token_serializer().loads(
            token, max_age=_MAX_TOKEN_AGE)
    except BadSignature:
        abort(401)

    return jsonify({
        'auth_token': token,
        'user_info': token_data['user_info'],
    })
