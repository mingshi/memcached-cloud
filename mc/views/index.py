# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from mc.model import *
from mc.db.db import db_session

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    return render_template("mc/index.html", server_count = db_session.query(Memcacheds).count())

    # from memcacheserver import memcache_servers
    # server = []
    # for sid in memcache_servers :
    #     try :
    #         instance_addr = memcache_servers[sid]['addr']
    #         instance_addr = instance_addr.split(':')
    #         instance_ip = instance_addr[0]
    #         server.append(instance_ip)
    #     except Exception, e : 
    #         server.append('null')
    # from collections import Counter
    # ser = Counter(server)
    # return render_template("mc/index.html", 
    #         instance_count = len(memcache_servers),
    #         host_count = len(ser)
    #         )

