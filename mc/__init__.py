# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, render_template
from mc.views import index, server
import os
app = Flask(__name__)

# load config according to enviroment
app.config.from_object("config")
if os.path.exists(app.config['ROOT_PATH'] + "/env.py"):
    app.config.from_object("env")

app.config.from_object("config.%sConfig" % (app.config['ENV']) )

from mc.db.db import db_session

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

