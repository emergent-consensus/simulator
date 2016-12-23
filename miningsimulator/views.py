from flask import Flask, request, session, Response, redirect, url_for, render_template, json
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from app import miners
import uuid
from flask_socketio import SocketIO, emit

app = Flask(__name__)

connections = dict()
sessions = dict()

Bootstrap(app)
socketio = SocketIO(app)

rigs = [miners.MiningRig(123), miners.MiningRig(456), miners.MiningRig(789), miners.MiningRig(532), miners.MiningRig(10)]

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
    global connections
    response = dict()
    response["count"] = len(connections)
    print "Sending connection message "
    socketio.broadcast.emit('connection', response, namespace="/mining")

@socketio.on('connect', namespace='/mining')
def connect():
    send_connection()
    print('message connection')

@socketio.on('disconnect', namespace='/mining')
def disconnect():
    global sessions
    global connections
    if request.sid in sessions:
        userid = sessions[request.sid]
        connections[userid].remove(request.sid)
        if len(connections[userid]) == 0:
            del connections[userid]
        del sessions[request.sid]
    send_connection()

@socketio.on('identify', namespace='/mining')
def identify(data):
    print str(data)
    print "identify"
    global connections
    global sessions
    if "userid" in data:
        print data["userid"]
        if data["userid"] in connections:
            connections[data["userid"]].append(request.sid)
            print "appending"
        else:
            connections[data["userid"]] = [request.sid]
            print "setting new"
        sessions[request.sid] = data["userid"]
    print len(connections)

if __name__ == "__main__":
    socketio.run(app)