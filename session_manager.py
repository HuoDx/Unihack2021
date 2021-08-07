from uuid import uuid4


rev_sessions = {}

def add_session(user_uid: str):
    global rev_sessions
    session = str(uuid4())
    rev_sessions.update({session: user_uid})
    return session

def get_uid(session):
    global rev_sessions
    return rev_sessions.get(session, None)

