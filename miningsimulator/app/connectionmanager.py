from user import User
import uuid

class ConnectionManager:
    
    def __init__(self, socketapi, network):
        self._sessions = dict()
        self._users = dict()
        self._socketapi = socketapi
        self._network = network

    def add_user(self, userid, sessionid):
        self._sessions[sessionid] = userid
        if userid in self._sessions:
            self._users[userid].add_session(sessionid)
        else:
            self._users[userid] = User(sessionid)
        self._socketapi.send_connection_update(len(self._users))

        user = self._users[userid]
        if len(user._miningrigs) == 0:
            #For now, assign a mining rig to a user that is identified
            self._network.add_miner(100, user)

        best_nodes = []
        for one_block in self._network.current_tips:
            best_nodes.append({"id": one_block.id.hex, "height": one_block.height, "miner": ""})
        self._socketapi.update_best_nodes(best_nodes, sessionid)
   

    def disconnect(self, sessionid):
        if sessionid in self._sessions:
            userid = self._sessions[sessionid]
            self._users[userid].remove_session(sessionid)
            if userid in self._users and len(self._users[userid].sessions) == 0:
                del self._users[userid]
            del self._sessions[sessionid]
        self._socketapi.send_connection_update(len(self._users))

    def num_users(self):
        return len(self._users)

    def get_or_set_cookie(self, cookies, response):
        if not 'userid' in cookies: 
            cookie = uuid.uuid4()
            response.set_cookie('userid', cookie.hex)
            return cookie
        return uuid.UUID(cookies['userid'])

