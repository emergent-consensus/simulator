from flask import Flask, request, session, Response, redirect, url_for, render_template, json
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from app import miners, connectionmanager, block
import uuid
from flask_socketio import SocketIO, emit
import os

import logging
logging.basicConfig()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import random

app = Flask(__name__)

connectionmanager = connectionmanager.ConnectionManager()

genesis_block = block.Block(None, uuid.uuid4())
print "Genesis Block: " + genesis_block.id.hex

longest_blocks = [genesis_block]

Bootstrap(app)
socketio = SocketIO(app)

rigs = [miners.MiningRig(123), miners.MiningRig(456), miners.MiningRig(789), miners.MiningRig(532), miners.MiningRig(10)]


apsched = BackgroundScheduler()
  
def pick_new_block(user):
    global longest_blocks
    block_saw_first = longest_blocks[sysrandom.randint(0, len(longest_blocks)-1)]
    user.miningblock = block_saw_first
    print "Updating Block for user " + user._userid + " block " + block_saw_first.id.hex
    return block_saw_first


def on_block_found(block):
    socketio.emit("block-found", {"id": block.id.hex, "height": block.height, "miner": block.miner.user.userid.hex, "parentid": block.miner.user.miningblock.id.hex})

def checkForBlocks():
    difficulty = 10 * connectionmanager.num_users()
    new_blocks = []
    missing_users = []
    for userid in connectionmanager._users:
        user = connectionmanager._users[userid]
        if sysrandom.randint(0, difficulty) == 0:
            found = block.Block(user.miningblock, uuid.uuid4())
            new_blocks.append(found)
            block_data = {"id": found.id.hex, "height": found.height, "miner": userid, "parentid": user.miningblock.id.hex}
            user.miningblock = found
            print "emitting"
            socketio.emit('block-found', block_data, namespace="/mining")
            print "Found Block " + found.id.hex + " for user " + userid
            print "Height " + str(found.height)
        else:
            missing_users.append(user)

    num_blocks_found = len(new_blocks)
    if num_blocks_found > 0:
        global longest_blocks
        print longest_blocks
        longest_blocks = new_blocks
        for user in missing_users:
            pick_new_block(user)

    else:
        print "no blocks were found"



apsched.add_job(
    func=checkForBlocks,
    trigger=IntervalTrigger(seconds=1))
apsched.start()


@app.route("/")
def main_page():
    return network_page()

@app.route("/network")
def network_page():
    response = app.make_response(render_template('network.html'))
    cookie = get_and_set_cookie(request, response)
    return response

@app.route("/my-rigs")
def myrig_page():
    return render_template('my_rigs.html', rigs= rigs)

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
    found = pick_new_block(user)
    best_nodes = []
    for one_block in longest_blocks:
        best_nodes.append({"id": one_block.id.hex, "height": one_block.height, "miner": ""})
    socketio.emit('best-nodes', best_nodes, room=request.sid, namespace='/mining')
   
if __name__ == "__main__":
    socketio.run(app)