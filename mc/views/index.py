# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from mc.model import *

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    memcache_servers = Memcacheds.query.all()
    return render_template("mc/index.html", server_count = len(memcache_servers))

