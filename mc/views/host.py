from flask import Blueprint, render_template, request
from mc.db.db import db_session
from mc.model import *

mod = Blueprint("host", __name__)

@mod.route('/hosts')
def hosts_index():
    from sqlalchemy import func
    hosts = db_session.query(Memcacheds.ip, func.count(Memcacheds.ip).label('memcached_count')).group_by(Memcacheds.ip).all()
    
    return  render_template('mc/host_index.html', hosts = hosts)












