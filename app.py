from flask import Flask, send_from_directory
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
