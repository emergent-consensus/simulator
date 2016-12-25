from user import User

class ConnectionManager:
    
    def __init__(self):
        self._sessions = dict()
        self._users = dict()

    def add_user(self, userid, sessionid):
        self._sessions[sessionid] = userid
        if userid in self._sessions:
            self._users[userid].add_session(sessionid)
        else:
            self._users[userid] = User(sessionid)

    def disconnect(self, sessionid):
        if sessionid in self._sessions:
            userid = self._sessions[sessionid]
            self._users[userid].remove_session(sessionid)
            if userid in self._users and len(self._users[userid].sessions) == 0:
                del self._users[userid]
            del self._sessions[sessionid]

    def num_users(self):
        return len(self._users)

