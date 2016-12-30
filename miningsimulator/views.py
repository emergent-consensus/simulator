from flask import Flask, request, Response, render_template
from flask_bootstrap import Bootstrap
from app import connectionmanager, miningnetwork, socketapi
app = Flask(__name__)

from flask_socketio import SocketIO
import os

import logging
logging.basicConfig()

app = Flask(__name__)

Bootstrap(app)
socketio = SocketIO(app)
sockets = socketapi.SocketAPI(socketio)

def on_block_found(block):
    sockets.send_block_found(block)
    print block

network = miningnetwork.MiningNetwork(on_block_found, None)
connectionmanager = connectionmanager.ConnectionManager(sockets, network)

@app.route("/")
def main_page():
    return network_page()

@app.route("/network")
def network_page():
    response = app.make_response(render_template('network.html'))
    connectionmanager.get_or_set_cookie(request.cookies, response)
    return response

@socketio.on('disconnect', namespace='/mining')
def disconnect():
    connectionmanager.disconnect(request.sid)

@socketio.on('identify', namespace='/mining')
def identify(data):
    connectionmanager.add_user(data["userid"], request.sid)
   
if __name__ == "__main__":
    socketio.run(app)