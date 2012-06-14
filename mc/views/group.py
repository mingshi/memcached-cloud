from flask import Blueprint, render_template, request
from cache.cache_server import Client
from mc.db.db import db_session
from mc.model import *
import json

mod = Blueprint("group", __name__)

@mod.route('/groups')
def groups_index():
    from sqlalchemy import func
    groups = db_session.query(Groups, func.sum(Memcacheds.memory).label('group_total_memory'),func.count(Memcacheds.ip).label('memcached_count')) \
        .outerjoin(Memcacheds, Memcacheds.group_id == Groups.id) \
        .group_by(Groups.id).all()
    stats_hit = {}
    for group in groups :
        group_get = 0
        group_hit = 0
        memcacheds = db_session.query(Memcacheds).filter_by(group_id = group.Groups.id).all()
        for memcached in memcacheds :
            try :
                addr = memcached.ip + ":" + str(memcached.port)
                client = Client([addr])
                stats = client.get_stats()[0][1]
                stats['cmd_get'] = int(stats['cmd_get'])
                stats['get_hits'] = int(stats['get_hits'])
            except Exception, e :
                continue
            group_get += int(stats['cmd_get'])
            group_hit += float(stats['get_hits'])
        if (group_get != 0) :
            stats_hit[group.Groups.id] = {"hit": round(((group_hit / group_get) * 100),2)}
        else :
            stats_hit[group.Groups.id] = {"hit": "/"}
    return  render_template('mc/groups_index.html', groups = groups, stats_hit = stats_hit)

@mod.route('/group-add')
def group_add():
    
    return  render_template('mc/group_add.html')

@mod.route('/group/do_add', methods=['GET','POST'])
def group_do_add() :
    result = {}

    if not request.form.has_key('name') :
        result['status'] = 'error'
        result['message'] = 'please input name'
    else :
        name = request.form['name']
        count = db_session.query(Groups).filter_by(name = name).count()
        if (count > 0) :
            result['status'] = 'error'
            result['message'] = 'group ' + name + ' is existed!'
        else :
            group = Groups(name)
            db_session.add(group)
            db_session.commit()
            result['status'] = 'ok'
            result['message'] = 'add successed. group id is ' + str(group.id)

    return json.dumps(result)

