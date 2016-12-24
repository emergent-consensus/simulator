class ConnectionManager:
    
    def __init__(self):
        self._sessions = dict()
        self._users = dict()

    def add_user(self, userid, sessionid):
        self._sessions[sessionid] = userid
        if userid in self._sessions:
            self._users[userid].append(sessionid)
        else:
            self._users[userid] = [sessionid]
        print self._sessions
        print self._users

    def disconnect(self, sessionid):
        if sessionid in self._sessions:
            userid = self._sessions[sessionid]
            self._users[userid].remove(sessionid)
            if userid in self._users and len(self._users[userid]) == 0:
                del self._users[userid]
            del self._sessions[sessionid]
        print self._sessions
        print self._users
            
    def num_users(self):
        return len(self._users)

