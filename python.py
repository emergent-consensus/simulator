from flask import Flask
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from flask import render_template
from app import miners

app = Flask(__name__)
Bootstrap(app)

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

if __name__ == "__main__":
    app.run()