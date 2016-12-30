class User:
    def __init__(self, userid):
        self._userid = userid
        self._miningrigs = []
        self.sessions = []
        self.blocks_found = 0
    
    def add_session(self, sessionid):
        self.sessions.append(sessionid)
    
    def remove_session(self, sessionid):
        if sessionid in self.sessions:
            self.sessions.remove(sessionid)

    def set_parent(self, blockid):
        self.miningblock = blockid

    def __str__(self):
        return self._userid