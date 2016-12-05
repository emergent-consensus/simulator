from flask import Flask
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from flask import render_template


app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/network")
def network_page():
    return render_template('network.html')

@app.route("/my-rigs")
def myrig_page():
    return render_template('my_rigs.html')

if __name__ == "__main__":
    app.run()