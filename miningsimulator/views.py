from flask import Flask, request, session, Response, redirect, url_for, render_template, json
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from app import miners, connectionmanager
import uuid
from flask_socketio import SocketIO, emit

app = Flask(__name__)

connectionmanager = connectionmanager.ConnectionManager()

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
  
if __name__ == "__main__":
    socketio.run(app)