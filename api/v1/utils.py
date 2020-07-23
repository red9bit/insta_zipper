import json


def create_auth_response(status, message, **kwargs):
    response = {
        'status': status,
        'error': message,
        **kwargs
    }
    return json.dumps(response)
