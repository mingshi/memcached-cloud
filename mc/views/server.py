from flask import Blueprint, render_template, request
import jinja2
import os
from memcacheserver import memcache_servers
from cache.cache_server import Client
from mc.utils.str import human_readable_size
from mc.db.db import db_session
from mc.model import *

jinja2.filters.FILTERS['human_readable_size'] = human_readable_size

import json

mod = Blueprint("server", __name__)

@mod.route('/hosts')
def hosts_index():
    server = []
    for sid in memcache_servers :
        try :
            instance_addr = memcache_servers[sid]['addr']
            instance_addr = instance_addr.split(':')
            instance_ip = instance_addr[0]
            server.append(instance_ip)
        except Exception, e :
            server.append('null')
    from collections import Counter
    ser = Counter(server)
    return  render_template('mc/server_index.html', servers = ser)












