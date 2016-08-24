import http
from flask import Blueprint, jsonify, abort
from ..models import db, User, Role


roles = Blueprint("roles", __name__, template_folder="templates")

@roles.route('', methods=['GET'])
def get_all():
    role_modals = db.session.query(Role)
    return jsonify({'data':[r.to_list() for r in role_modals]})


@roles.route('/<int:role_id>', methods=['GET'])
def get(role_id):
    role = db.session.query(Role).filter_by(id=role_id).first()
    if not role:
        abort(http.client.NOT_FOUND)
    return jsonify({'data': role.to_dict()})
