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
    memcacheds = db_session.query(Memcacheds).order_by(Memcacheds.group_id).order_by(Memcacheds.id).all()
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
            status = 'ok'
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

@mod.route('/memcacheds-<group_id>')
def memcacheds_group(group_id):
    memcacheds = db_session.query(Memcacheds).filter_by(group_id = group_id).order_by(Memcacheds.id).all()
    groups = db_session.query(Groups).filter_by(id = group_id).all()

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
            status = 'ok'
        except Exception, e : 
            status = 'error'

        _memcacheds.append({"id":_memcached.id, 
            "ip":ip, 
            "port":port, 
            'status':status, 
            'group_id' : _memcached.group_id,
            'group_name' : group_names[_memcached.group_id] if group_names.has_key(_memcached.group_id) else  '/' 
            })  
    return render_template('mc/memcacheds_group.html', memcacheds = _memcacheds, group_names = group_names, group_id = group_id)

@mod.route('/memcached-add', methods=['GET','POST'])
def memcached_add() :
    groups = db_session.query(Groups).all()
    group_names = {}
    for _group in groups :
        group_names[_group.id] = _group.name
    return render_template('mc/memcached_add.html', group_names = group_names)

@mod.route('/memcached/check', methods=['GET','POST'])
def memcached_check() :
    result = {}
    if not request.form.has_key('ip') :
        result['status'] = '0'
    elif not request.form.has_key('port') :
        result['status'] = '0'
    else :
        ip = request.form['ip'].strip().encode('utf8')
        port = str(request.form['port'].strip())
        _memcached = db_session.query(Memcacheds).filter_by(ip = ip,port = port).first()
        if not _memcached :
            result['status'] = '1'
        else :
            result['status'] = '0'
    return json.dumps(result)

@mod.route('/memcached/do_add', methods=['GET','POST'])
def memcached_do_add() :
    result = {}
    if not request.form.has_key('ip') :
        result['status'] = 'no ip address'
    elif not request.form.has_key('version') :
        result['status'] = 'no version selected'
    elif not request.form.has_key('port') :
        result['status'] = 'no port inputed'
    elif not request.form.has_key('memory') :
        result['status'] = 'no memory inputed'
    elif not request.form.has_key('group') :
        result['status'] = 'no group selected'
    else :
        ip = request.form['ip'].strip().encode('utf8')
        version = request.form['version']
        port = str(request.form['port'].strip())
        memory = str(request.form['memory'].strip())
        group = str(request.form['group'])
        param = request.form['param'].strip().encode('utf8')
        isstart = str(request.form['isstart'])
        _memcached = db_session.query(Memcacheds).filter_by(ip = ip,port = port).first()
        if not _memcached :
            if not param :
                data = os.popen("bash /var/www/memcache_cloud/memcached_add.sh " + ip + " " + version + " " + port + " " + memory + " " + isstart).read()
            else :
                data = os.popen("bash /var/www/memcache_cloud/memcached_add.sh " + ip + " " + version + " " + port + " " + memory + " " + isstart + " '" + param + "'").read()
            result['status'] = data
            if (isstart == "1" and data == "add success\n") or isstart == "0" :
                memcache = Memcacheds(ip=ip, port=port, memory=memory, status=1, group_id=group, version=version, parameters=param)
                db_session.add(memcache)
                #db_session.commit()
        else :
            result['status'] = 'the memcached is already added'
    return json.dumps(result)


@mod.route('/memcached/do_edit', methods=['GET', 'POST'])
def memcached_do_edit() :
    result = {}
    memcached_id = int(request.form['memcached_id'])
    ip = request.form['ip'].strip().encode('utf8')
    version = int(request.form['version'])
    port = int(request.form['port'].strip())
    memory = int(request.form['memory'].strip())
    group = int(request.form['group'])
    param = request.form['param'].strip().encode('utf8')
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    _memcached.ip = ip
    _memcached.version = version
    _memcached.port = port
    _memcached.memory = memory
    _memcached.group_id = group
    _memcached.parameters = param
    #db_session.commit()
    result['status'] = 'Edit success!'
    return json.dumps(result)

@mod.route('/memcached-<memcached_id>-stop', methods=['GET', 'POST'])
def memcached_stop(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'

    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    result = {}
    if not _memcached :
        result['status'] = "the memcached not exist"
    else :
        data = os.popen("bash /var/www/memcache_cloud/memcached_stop.sh " + _memcached.ip + " " + str(_memcached.port) + " " + str(_memcached.memory) + " " + str(_memcached.version) + " '" + str(_memcached.parameters) + "'").read()
        result['status'] = data
        _memcached.status = 0
        #db_session.commit()
    return json.dumps(result)

@mod.route('/memcached-<memcached_id>-delete', methods=['GET', 'POST'])
def memcached_delete(memcached_id) :
    result = {}
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    db_session.delete(_memcached)
    #db_session.commit()
    result['status'] = 'delete success'
    return json.dumps(result)

@mod.route('/memcached-<memcached_id>-start', methods=['GET', 'POST'])
def memcached_start(memcached_id) :
    result = {}
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    if not _memcached :
        result['status'] = "the memcached not exist"
    else :
        data = os.popen("bash /var/www/memcache_cloud/memcached_start.sh " + _memcached.ip + " " + str(_memcached.port) + " " + str(_memcached.memory) + " " + str(_memcached.version) + " '" + str(_memcached.parameters) + "'").read()
        result['status'] = data
        _memcached.status = 1
        #db_session.commit()
    return json.dumps(result)

@mod.route('/memcached-<memcached_id>-restart', methods=['GET', 'POST'])
def memcached_restart(memcached_id) :
    result = {}
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    if not _memcached :
        result['status'] = "the memcached not exist"
    else :
        data = os.popen("bash /var/www/memcache_cloud/memcached_restart.sh " + _memcached.ip + " " + str(_memcached.port) + " " + str(_memcached.memory) + " " + str(_memcached.version) + " '" + str(_memcached.parameters) + "'").read()
        result['status'] = data
        _memcached.status = 1
        #db_session.commit()
    return json.dumps(result)

@mod.route('/memcached-edit-<memcached_id>', methods=['GET', 'POST'])
def memcached_edit(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'
    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    groups = db_session.query(Groups).all()
    group_names = {}
    for _group in groups :
        group_names[_group.id] = _group.name
    return render_template('mc/memcached_edit.html', memcached = _memcached,group_names = group_names)

@mod.route('/memcached-<memcached_id>')
def memcached_detail(memcached_id) :
    try :
        memcached_id = int(memcached_id)
    except Exception, e :
        return 'invalid memcached id'

    _memcached = db_session.query(Memcacheds).filter_by(id = memcached_id).first()
    addr =  _memcached.ip + ':' + str(_memcached.port)

    client = Client([addr])
    temp = client.get_stats('slabs')
    if temp == None  or len(temp) == 0:
        return render_template("mc/memcached_err.html", addr = addr)
    slabs = temp[0]
    _slabs = client.get_slabs()[0][1]

    slabs_stats = []
    from pprint import pprint
    for slab_id in slabs :
        try :
            int(slab_id)
        except Exception, e :
            continue

        chunk_size = int(slabs[slab_id]['chunk_size'])

        _slabs_stats = {
            'slab_id' : int(slab_id), 
            'used_chunks' : int(slabs[slab_id]['used_chunks']),
            'free_chunks' : int(slabs[slab_id]['free_chunks']) + int(slabs[slab_id]['free_chunks_end']),
            'evicted' :  int(_slabs[slab_id]['evicted']) if _slabs.has_key(slab_id) and  _slabs[slab_id].has_key('evicted') else  0,
            'get_hits' : int(slabs[slab_id]['get_hits']) if slabs[slab_id].has_key('get_hits') else '/',
            'size' : human_readable_size(chunk_size)
            }

        _slabs_stats['used_size'] = human_readable_size(chunk_size * _slabs_stats['used_chunks'])
        _slabs_stats['free_size'] = human_readable_size(chunk_size * _slabs_stats['free_chunks'])

        if (_slabs_stats['get_hits'] != '/' and _slabs_stats['get_hits'] != 0) :
            _slabs_stats['evicted_rate'] = str(round(float(_slabs_stats['evicted']) / _slabs_stats['get_hits'] * 100, 2))
            _slabs_stats['evicted_rate'] += '%'
        else :
            _slabs_stats['evicted_rate'] = '/'


        slabs_stats.append(_slabs_stats)

    #print slabs_stats
    slabs_stats.sort(key = lambda x: x['slab_id'])
    slabs_stats_str = json.dumps(slabs_stats)

    stats = client.get_stats()[0][1]
    stats_str = json.dumps(stats)

    hits_stats = [{'type':'hits', 'color':'#669900', 'value' : stats['get_hits']}, { 'type':'misses', 'color':'#ff0000', 'value' : stats['get_misses']}]
    hits_stats_str = json.dumps(hits_stats)

    from pprint import pprint

    return render_template("mc/memcached_detail.html", 
            memcached_id = memcached_id,
            addr = addr,
            memcached = _memcached,
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


@mod.route('/memcached/group-data/<group_id>', methods=['GET', 'POST'])
def memcached_data(group_id) :
    try :
        group_id = int(group_id)
    except Exception, e :
        return json.dumps({"status":"error", 'msg':'invalid group id'})

    if not request.form.has_key('key') :
        return json.dumps({"status":"error", 'msg':'no key input'})

    key = request.form['key'].encode('utf8')

    action = ""
    if request.form.has_key('action') :
        action = request.form["action"].encode('utf8')

    memcacheds = db_session.query(Memcacheds).filter_by(group_id = group_id).order_by(Memcacheds.id).all()

    result = {}
    if action == 'delete' :
        client.delete(key)
        result['status'] = 'ok'
    else :
        result['status'] = 'ok'
        result['data'] = {}

        for _memcached in memcacheds :
            addr =  _memcached.ip + ':' + str(_memcached.port)
            client = Client([addr])
            result['data'][addr] = client.get(key)

    return json.dumps(result)
