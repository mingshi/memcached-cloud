
from flask import Blueprint, render_template

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    from memcacheserver import memcache_servers
    return render_template("mc/index.html", server_count = len(memcache_servers))
