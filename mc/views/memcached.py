from flask import Blueprint, render_template, request
import jinja2
import os
from cache.cache_server import Client
from mc.utils.str import human_readable_size
from mc.db.db import db_session
from mc.model import *

jinja2.filters.FILTERS['human_readable_size'] = human_readable_size

import json

mod = Blueprint("memcached", __name__)

@mod.route('/memcacheds')
def memcacheds_index():
    memcacheds = db_session.query(Memcacheds).all()
    groups = db_session.query(Groups).all()

    import socket
    _memcacheds = []
    group_names = {}
    for _group in groups :
        group_names[_group.id] = _group.name

    for _memcached in memcacheds :
        try :
            ip = _memcached.ip
            port = _memcached.port
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(0.01)
            address = (str(ip),int(port))
            status = sk.connect((address))
            print address
        except Exception, e :
            status = 'error'

        _memcacheds.append({"id":_memcached.id, 
            "ip":ip, 
            "port":port, 
            'status':status, 
            'group_id' : _memcached.group_id,
            'group_name' : group_names[_memcached.group_id] if group_names.has_key(_memcached.group_id) else  '/'
            })
    return render_template('mc/memcacheds_index.html', memcacheds = _memcacheds, group_names = group_names)


@mod.route('/memcached-add', methods=['GET','POST'])
def memcached_add() :
    return render_template('mc/memcached_add.html')

@mod.route('/memcached/do_add', methods=['GET','POST'])
def memcached_do_add() :
    result = {}
    if not request.form.has_key('ip') :
        result['status'] = 'no ip address'
    elif not request.form.has_key('version') :
        result['status'] = 'no version selected'
    elif not request.form.has_key('param') :
        result['status'] = 'no param inputed'
    else :
        host = request.form['ip'].strip().encode('utf8')
        version = request.form['version']
        param = request.form['param'].strip().encode('utf8')
        data = os.popen("bash instance_add.sh " + host + " " + version + " '" + param + "'").read()
        result['status'] = data
    return json.dumps(result)


@mod.route('/memcached-<memcached_id>-stop', methods=['GET', 'POST'])
def memcached_stop(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'

    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    addr =  _memcached.ip + ':' + str(_memcached.port)

    addr = addr.split(':')
    result = {}
    res = os.system("ssh " + addr[0] + " 'ps -ef|grep memcached|grep " + addr[1] + "|grep -v grep|awk " + "'" + "\\" + "'\$2!=" + addr[1] + "{print \$2}" + "\\''|xargs kill'")
    if res == 0 :
        result['status'] = 'ok'
    else :
        result['status'] = 'error'
    return json.dumps(result)


@mod.route('/memcached-<memcached_id>')
def memcached_detail(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'

    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    addr =  _memcached.ip + ':' + str(_memcached.port)

    client = Client([addr])
    slabs = client.get_stats('slabs')[0]
    _slabs = client.get_slabs()[0][1]

    slabs_stats = []
    from pprint import pprint
    for slab_id in slabs :
        try :
            int(slab_id)
        except Exception, e :
            continue
        slabs_stats.append({
            'slab_id' : int(slab_id), 
            'used_chunks' : slabs[slab_id]['used_chunks'],
            'free_chunks' : int(slabs[slab_id]['free_chunks']) + int(slabs[slab_id]['free_chunks_end']),
            'evicted' :  _slabs[slab_id]['evicted'] if _slabs.has_key(slab_id) and  _slabs[slab_id].has_key('evicted') else  0,
            'size' : human_readable_size(slabs[slab_id]['chunk_size'])
            })

    #print slabs_stats
    slabs_stats.sort(key = lambda x: x['slab_id'])
    slabs_stats_str = json.dumps(slabs_stats)

    stats = client.get_stats()[0][1]
    stats_str = json.dumps(stats)

    hits_stats = [{'type':'hits', 'color':'#00ff00', 'value' : stats['get_hits']}, { 'type':'misses', 'color':'#ff0000', 'value' : stats['get_misses']}]
    hits_stats_str = json.dumps(hits_stats)

    from pprint import pprint

    return render_template("mc/memcached_detail.html", 
            memcached_id = memcached_id,
            addr = addr, 
            slabs_stats = slabs_stats,
            slabs_stats_str = slabs_stats_str,
            stats = stats,
            stats_str = stats_str,
            hits_stats_str = hits_stats_str)

@mod.route('/memcached_slab_key-<memcached_id>-<slab_id>')
def memcached_slab_keys(memcached_id, slab_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    addr =  _memcached.ip + ':' + str(_memcached.port)

    client = Client([addr])
    keys = client.get_key_prefix(slab_id)

    return json.dumps(keys)

@mod.route('/memcached/data/<memcached_id>', methods=['GET', 'POST'])
def memcached_data(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return json.dumps({"status":"error", 'msg':'invalid memcached id'})

    if not request.form.has_key('key') :
        return json.dumps({"status":"error", 'msg':'no key input'})

    key = request.form['key'].encode('utf8')

    action = ""
    if request.form.has_key('action') :
        action = request.form["action"].encode('utf8')

    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    addr =  _memcached.ip + ':' + str(_memcached.port)

    client = Client([addr])

    result = {}
    if action == 'save' :
        if not request.form.has_key('data') :
            result['status'] = 'error'
            result['msg'] = 'no data input'
        else:
            data = request.form['data']
            client.set(key, data)
            result['status'] = 'ok'
    elif action == 'delete' :
        client.delete(key)
        result['status'] = 'ok'
    else :
        result['status'] = 'ok'
        result['data'] = client.get(key)

    return json.dumps(result)
