from jsonschema import Draft4Validator
from functools import wraps
from flask import request, abort, Blueprint as FlaskBlueprint
import logbook
import http.client


def validate_schema(schema):
    validator = Draft4Validator(schema)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(http.client.BAD_REQUEST)

            try:
                validator.validate(request.json)
            except Exception as e:
                logbook.error(e)
                abort(http.client.BAD_REQUEST)

            return f(*args, **kwargs)
        return wrapper
    return decorator
