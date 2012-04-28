from flask import Blueprint, render_template
from memcacheserver import memcache_servers

from cache.cache_server import Client
import json

mod = Blueprint("server", __name__)

@mod.route('/servers')
def server_index():
    return render_template('mc/server_index.html', servers = memcache_servers)

@mod.route('/server-<sid>')
def server_detail(sid) :
    try :
        sid = int(sid)
    except Exception, e :
        return 'invalid server id'

    addr = memcache_servers[sid]
    client = Client([addr])
    slabs = client.get_stats('slabs')[0]
    slabs_stats = []
    from pprint import pprint
    for slab_id in slabs :
        try :
            int(slab_id)
        except Exception, e :
            continue
        slabs_stats.append({'slab_id' : int(slab_id), 'chunks' : slabs[slab_id]['used_chunks'] })

    #print slabs_stats
    slabs_stats.sort(key = lambda x: x['slab_id'])
    

    slabs_stats_str = json.dumps(slabs_stats)
    
    print slabs_stats_str

    return render_template("mc/server_detail.html", 
            addr = addr, 
            slabs = slabs, 
            slabs_stats_str = slabs_stats_str)
