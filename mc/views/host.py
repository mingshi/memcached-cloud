from flask import Blueprint, render_template, request
from mc.db.db import db_session
from mc.model import *
import os
import json

mod = Blueprint("host", __name__)

@mod.route('/hosts')
def hosts_index():
    from sqlalchemy import func
    hosts = db_session.query(Memcacheds.ip, func.count(Memcacheds.ip).label('memcached_count')).group_by(Memcacheds.ip).all()
    return  render_template('mc/host_index.html', hosts = hosts)

@mod.route('/host/info', methods=['GET','POST'])
def host_info() :
    result = {}
    ip = request.form['ip'].strip().encode('utf8')
    total_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + ip + " cat /proc/meminfo|grep MemTotal|awk '{print $2}'").read().strip()
    total_mem = round((float(total_mem) / 1024 / 1024),2)
    free_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + ip + " cat /proc/meminfo|grep MemFree|awk '{print $2}'").read().strip()
    free_mem = round((float(free_mem) / 1024 / 1024),2)
    cache_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + ip + " cat /proc/meminfo|grep Cached|head -1|awk '{print $2}'").read().strip()
    cache_mem = round((float(cache_mem) / 1024 / 1024),2)
    result['total'] = total_mem
    result['free'] = free_mem
    result['cache'] = cache_mem
    return json.dumps(result)










