from flask import Flask, request, session, Response, redirect, url_for, render_template, json
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from app import miners, connectionmanager, block, miningnetwork
import uuid
from flask_socketio import SocketIO, emit
import os

import logging
logging.basicConfig()

app = Flask(__name__)


connectionmanager = connectionmanager.ConnectionManager()

Bootstrap(app)
socketio = SocketIO(app)

def on_block_found(block):
    id = block.id.hex
    miner = block.miner.user._userid
    parentid = block.parent.id.hex
    socketio.emit("block-found", {"id": block.id.hex, "height": block.height, "miner": block.miner.user._userid, "parentid": block.parent.id.hex}, namespace="/mining")
    print block

def on_block_not_found():
    print "Block not found"

network = miningnetwork.MiningNetwork(on_block_found, on_block_not_found)

@app.route("/")
def main_page():
    return network_page()

@app.route("/network")
def network_page():
    response = app.make_response(render_template('network.html'))
    cookie = get_and_set_cookie(request, response)
    return response

@app.route("/graph")
def graph_page():    
    return render_template('graph.html')

def get_and_set_cookie(request, response):
    if not 'userid' in request.cookies: 
        cookie = uuid.uuid4()
        response.set_cookie('userid', cookie.hex)
        return cookie
    return uuid.UUID(request.cookies['userid'])

def send_connection():
    response = dict()
    response["count"] = str(connectionmanager.num_users())
    print "Sending connection message " + response["count"]
    socketio.emit('connection', response, namespace="/mining")

@socketio.on('disconnect', namespace='/mining')
def disconnect():
    connectionmanager.disconnect(request.sid)
    send_connection()

@socketio.on('identify', namespace='/mining')
def identify(data):
    connectionmanager.add_user(data["userid"], request.sid)

    send_connection()
    user = connectionmanager._users[data["userid"]]

    users_miner = miners.MiningRig(100, user)
    network.add_miner(users_miner)
#    found = pick_new_block(user)
    best_nodes = []
    for one_block in network.current_tips:
        best_nodes.append({"id": one_block.id.hex, "height": one_block.height, "miner": ""})
    socketio.emit('best-nodes', best_nodes, room=request.sid, namespace='/mining')
   
if __name__ == "__main__":
    socketio.run(app)