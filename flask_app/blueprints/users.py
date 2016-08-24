import http
from flask import Blueprint, jsonify, abort
from ..models import db, User, Role


users = Blueprint("users", __name__, template_folder="templates")

@users.route('', methods=['GET'])
def get_all():
    user_models = db.session.query(User)
    return jsonify({'data': [u.to_dict() for u in user_models]})

@users.route('/by_email/<email>', methods=['GET'])
def get_by_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        abort(http.client.NOT_FOUND)
    return jsonify({'data': user.to_dict()})


@users.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(http.client.NOT_FOUND)
    return jsonify({'data': user.to_dict()})

def has_role(user, role):
    if isinstance(user, int):
        user = db.session.query.get(user)
        if user is None:
            return False
    user_roles = {r.name for r in user.roles}
    if 'admin' in user_roles:
        return True
    return role in user_roles
