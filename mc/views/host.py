from flask import Blueprint, render_template, request
from mc.db.db import db_session
from mc.model import *
import os

mod = Blueprint("host", __name__)

@mod.route('/hosts')
def hosts_index():
    from sqlalchemy import func
    hosts = db_session.query(Memcacheds.ip, func.count(Memcacheds.ip).label('memcached_count')).group_by(Memcacheds.ip).all()
    host_total_mem = {}
    host_free_mem = {}
    host_cache_mem = {}
    total_mem = 0
    free_mem = 0
    cache_mem = 0
    for host in hosts :
        total_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + host.ip + " cat /proc/meminfo|grep MemTotal|awk '{print $2}'").read().strip()
        total_mem = round((float(total_mem) / 1024 / 1024),2)
        free_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + host.ip + " cat /proc/meminfo|grep MemFree|awk '{print $2}'").read().strip()
        free_mem = round((float(free_mem) / 1024 / 1024),2)
        cache_mem = os.popen("ssh -o StrictHostKeyChecking=no evans@" + host.ip + " cat /proc/meminfo|grep Cached|head -1|awk '{print $2}'").read().strip()
        cache_mem = round((float(cache_mem) / 1024 / 1024),2)
        host_total_mem[host.ip] = total_mem
        host_free_mem[host.ip] = free_mem
        host_cache_mem[host.ip] = cache_mem
    
    return  render_template('mc/host_index.html', 
            hosts = hosts,
            host_total_mem = host_total_mem,
            host_free_mem = host_free_mem,
            host_cache_mem = host_cache_mem)












