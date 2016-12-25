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
sysrandom = random.SystemRandom()

rigs = [miners.MiningRig(123), miners.MiningRig(456), miners.MiningRig(789), miners.MiningRig(532), miners.MiningRig(10)]

@app.before_first_request
def before_request():
    print "init"
    apsched = BackgroundScheduler()

    apsched.add_job(
    func=checkForBlocks,
    trigger=IntervalTrigger(seconds=1))
    apsched.start()

def checkForBlocks():
    difficulty = 10 * connectionmanager.num_users()
    new_blocks = []
    missing_users = []
    for userid in connectionmanager._users:
        user = connectionmanager._users[userid]
        if sysrandom.randint(0, difficulty) == 0:
            found = block.Block(user.miningblock, uuid.uuid4())
            new_blocks.append(found)
            user.miningblock = found
            block_data = dict()
            block_data["id"] = found.id.hex
            block_data["height"] = found.height
            block_data["miner"] = userid
            socketio.emit('block-found', block_data, namespace="/mining")
            print "Found Block " + found.id.hex + " for user " + userid
            print "Height " + str(found.height)
        else:
            missing_users.append(user)

    num_blocks_found = len(new_blocks)
    if num_blocks_found > 0:
        for user in missing_users:
            block_saw_first = new_blocks[sysrandom.randint(0, len(new_blocks)-1)]
            user.miningblock = block_saw_first
            print "Updating Block for user " + user._userid + " block " + block_saw_first.id.hex
    else:
        print "no blocks were found"


    socketio.emit("tick", namespace="/mining")

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
    connectionmanager._users[data["userid"]].miningblock = genesis_block #TODO PICK RANDOM MAX HEIGHT BLOCK
    send_connection()
  
if __name__ == "__main__":
    socketio.run(app)