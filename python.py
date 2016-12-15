from flask import Flask, request, session
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from flask import render_template
from app import miners

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

connections = 0

Bootstrap(app)
socketio = SocketIO(app)


rigs = [miners.MiningRig(123), miners.MiningRig(456), miners.MiningRig(789), miners.MiningRig(532), miners.MiningRig(10)]

@app.route("/")
def hello():
    return network_page()

@app.route("/network")
def network_page():
    return render_template('network.html')

@app.route("/my-rigs")
def myrig_page():
    return render_template('my_rigs.html', rigs= rigs)

@app.route("/graph")
def graph_page():
    return render_template('graph.html')

@socketio.on('connect', namespace='/test')
def connect():
    print('connect ' + request.sid)

@socketio.on('my message', namespace='/test')
def message(data):
    bar = dict()
    bar["hello"] = "name"
    socketio.emit("reply", bar, namespace='/test')
    print('message ' + request.sid)


@socketio.on('disconnect', namespace='/test')
def disconnect():
    print('disconnect ' + request.sid)

if __name__ == "__main__":
    socketio.run(app)