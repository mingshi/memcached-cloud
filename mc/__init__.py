
from flask import Flask, send_from_directory, render_template
import os
app = Flask(__name__)
app.config.from_object("websiteconfig")

from mc.test import haha

from mc.views import index, server

app.register_blueprint(index.mod)
app.register_blueprint(server.mod)

@app.route("/version")
def hello():
    return "0.1"

@app.route('/app-path')
def app_path():
    return app.root_path


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static' ), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
