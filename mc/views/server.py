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
        slabs_stats.append({
            'slab_id' : int(slab_id), 
            'used_chunks' : slabs[slab_id]['used_chunks'],
            'free_chunks' : int(slabs[slab_id]['free_chunks']) + int(slabs[slab_id]['free_chunks_end'])
            })

    #print slabs_stats
    slabs_stats.sort(key = lambda x: x['slab_id'])
    slabs_stats_str = json.dumps(slabs_stats)

    stats = client.get_stats()[0][1]
    stats_str = json.dumps(stats)

    hits_stats = [{'type':'hits', 'color':'#00ff00', 'value' : stats['get_hits']}, { 'type':'misses', 'color':'#ff0000', 'value' : stats['get_misses']}]
    hits_stats_str = json.dumps(hits_stats)

    return render_template("mc/server_detail.html", 
            addr = addr, 
            slabs_stats_str = slabs_stats_str,
            stats = stats,
            stats_str = stats_str,
            hits_stats_str = hits_stats_str)
