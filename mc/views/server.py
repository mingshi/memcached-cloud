from flask import Blueprint, render_template, request
import jinja2
import os
from memcacheserver import memcache_servers
from cache.cache_server import Client
from mc.utils.str import human_readable_size

jinja2.filters.FILTERS['human_readable_size'] = human_readable_size

import json

mod = Blueprint("server", __name__)

@mod.route('/instances')
def instances_index():
    import socket
    for sid in memcache_servers :
        try :
            addr = memcache_servers[sid]['addr']
            addr = addr.split(':')
            ip = addr[0]
            port = addr[1]
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(0.01)
            address = (str(ip),int(port))
            status = sk.connect((address))
            memcache_servers[sid]['status'] = 'ok'
        except Exception, e :
            memcache_servers[sid]['status'] = 'error'
    return render_template('mc/instances_index.html', servers = memcache_servers)

@mod.route('/hosts')
def servers_index():
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

@mod.route('/host-add', methods=['GET','POST'])
def host_add() :
    return render_template('mc/host_add.html')

@mod.route('/instance-add', methods=['GET','POST'])
def instance_add() :
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
    return render_template('mc/instance_add.html', servers = ser)

@mod.route('/instance/do_add', methods=['GET','POST'])
def instance_do_add() :
    result = {}
    if not request.form.has_key('host') :
        result['status'] = 'no host has selected'
    elif not request.form.has_key('param') :
        result['status'] = 'no param has input'
    else :
        host = request.form['host'].strip().encode('utf8')
        param = request.form['param'].strip().encode('utf8')
        data = os.popen("bash instance_add.sh " + host + " '" + param + "'").read()
        result['status'] = data
    return json.dumps(result)

@mod.route('/host/do_install', methods=['POST','GET'])
def host_install() :
    result = {}
    if not request.form.has_key('ip') :
        result['status'] = 'no ip address'
    elif not request.form.has_key('version') :
        result['status'] = 'no version has selected'
    else :
        ip = request.form['ip'].strip().encode('utf8')
        version = str(request.form['version'])
        data = os.popen("bash host_install.sh " + ip + " " + version).read() 
        result['status'] = data
    return json.dumps(result)

@mod.route('/server_slab_key-<sid>-<slab_id>')
def server_slab_keys(sid, slab_id) :
    try :
        sid = int(sid)
    except Exception, e :
        return 'invalid server id'

    addr = memcache_servers[sid]['addr']
    client = Client([addr])
    keys = client.get_key_prefix(slab_id)

    return json.dumps(keys)

@mod.route('/instance-<sid>-stop', methods=['GET', 'POST'])
def instance_stop(sid) :
    try :
        sid = int(sid)
    except Exception, e :
        return 'invalid server id'
    addr = memcache_servers[sid]['addr'].strip()
    addr = addr.split(':')
    result = {}
    #query = "ssh " + addr[0] + " 'ps -ef|grep memcached|grep " + addr[1] + "|grep -v grep|awk " + "'" + "\\" + "'{print $2}" + "\\''|xargs kill'"
    res = os.system("ssh " + addr[0] + " 'ps -ef|grep memcached|grep " + addr[1] + "|grep -v grep|awk " + "'" + "\\" + "'\$2!=" + addr[1] + "{print \$2}" + "\\''|xargs kill'")
    if res == 0 :
        result['status'] = 'ok'
    else :
        result['status'] = 'error'
    return json.dumps(result)


@mod.route('/server/data/<sid>', methods=['GET', 'POST'])
def server_data(sid) :
    try :
        sid = int(sid)
    except Exception, e :
        return json.dumps({"status":"error", 'msg':'invalid server id'})

    if not request.form.has_key('key') :
        return json.dumps({"status":"error", 'msg':'no key input'})

    key = request.form['key'].encode('utf8')

    action = ""
    if request.form.has_key('action') :
        action = request.form["action"].encode('utf8')

    addr = memcache_servers[sid]['addr']
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


@mod.route('/server-<sid>')
def server_detail(sid) :
    try :
        sid = int(sid)
    except Exception, e :
        return 'invalid server id'

    addr = memcache_servers[sid]['addr']
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

    return render_template("mc/server_detail.html", 
            sid = sid,
            addr = addr, 
            slabs_stats = slabs_stats,
            slabs_stats_str = slabs_stats_str,
            stats = stats,
            stats_str = stats_str,
            hits_stats_str = hits_stats_str)
