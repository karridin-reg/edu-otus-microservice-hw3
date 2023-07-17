import logging
import uuid
import datetime
from jose import jwt


def setup_storage(app, private_key):
    app.storage = Storage(private_key)


class Storage:

    def __init__(self, private_key):
        self.private_key = private_key
        self.states = dict()
        self.sessions = dict()

    def create_state(self, req_url):
        key = str(uuid.uuid4())
        self.states[key] = {'req_url': req_url}
        return key

    def pop_state(self, key):
        if key not in self.states:
            return

        return self.states.pop(key)

    def create_session(self, *, username):
        key = str(uuid.uuid4())
        groups = ['users']

        claims = {"groups": groups,
                  "username": username,
                  "iss": "http://auth-service",
                  "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365),
                  "sub": key}
        logging.info(f'Claims: {claims}')
        jwt_token = jwt.encode(claims=claims, key='secret')

        self.sessions[key] = {
            'x-username': username,
            'authorization': jwt_token,
            'x-auth-token': jwt_token
        }

        return key

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
