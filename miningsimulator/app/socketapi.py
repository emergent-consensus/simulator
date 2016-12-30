class SocketAPI:

    def __init__(self, socketio):
        self._socketio = socketio

    def send_block_found(self, block):
        self._socketio.emit("block-found", {"id": block.id.hex, "height": block.height, "miner": block.miner.user._userid, "parentid": block.parent.id.hex}, namespace="/mining")

    def send_connection_update(self, number_of_users):
        self._socketio.emit('connection', {"count": number_of_users}, namespace="/mining")

    def update_best_nodes(self, best_nodes, sessionid):
        self._socketio.emit('best-nodes', best_nodes, room=sessionid, namespace='/mining')