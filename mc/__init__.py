

from flask import Flask, send_from_directory
import os
app = Flask(__name__)
app.config.from_object("websiteconfig")

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/app-path')
def app_path():
    return app.root_path


@app.route('/favicon.ico')
def favicon():
    #return 'test';
    #return os.path.join(app.root_path, 'static') + ' favicon.ico'
    return send_from_directory(os.path.join(app.root_path, 'static' ), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
