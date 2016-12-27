class Messages:
    def send_connections():
        response = {"count": str(connectionmanager.num_users())}
        socketio.emit('connection', response, namespace="/mining")