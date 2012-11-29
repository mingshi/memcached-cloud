# -*- coding: utf-8 -*-

from mc.db.db import db_session
from mc.model import *
from cache.cache_server import Client
import json
import os
import time


memcacheds = db_session.query(Memcacheds).order_by(Memcacheds.group_id).order_by(Memcacheds.id).all()

logs_dir = "/var/www/memcache_cloud/logs/"

for memcached in memcacheds :
    ip = memcached.ip
    port = memcached.port
    addr = str(ip) + ":" + str(port)
    try :
        client = Client([addr])
        stats = client.get_stats()[0][1]
        current_get = stats['cmd_get']
        current_hit = stats['get_hits']
        mid = memcached.id
        log_file = logs_dir + str(memcached.id) + "_data"
        if os.path.isfile(log_file) :
            filehandler = open(log_file,'r')
            old_data = filehandler.readline().rstrip()
            old_data_arr = old_data.split(' ')
            if len(old_data_arr) == 2 :
                old_get = old_data_arr[0]
                old_hit = old_data_arr[1]
            else :
                old_get = 0
                old_hit = 0
            filehandler.close()
            if int(current_get) >= int(old_get) :
                process_get = int(current_get) - int(old_get)
                process_hit = int(current_hit) - int(old_hit)
            else :
                process_get = int(current_get)
                process_hit = int(current_hit)
            if process_get == 0 :
                hit_rank = 0
            else :
                hit_rank = "%.2f" % (float(process_hit) / float(process_get))
                hit_rank = float(hit_rank) * 100
                hit_rank = "%.0f" % hit_rank
            nowtime = int(time.time())
            log = Logs(num=hit_rank,get=process_get,hit=process_hit,log_type=1,time=nowtime,m_id=mid)
            db_session.add(log)
            db_session.commit()
            this_data = str(current_get) + ' ' + str(current_hit)
            fw = open(log_file,'w')
            fw.write(this_data)
            fw.close()
        else :
            process_get = int(current_get)
            process_hit = int(current_hit)
            if process_get == 0 :
                hit_rank = 0
            else :
                hit_rank = "%.2f" % (float(process_hit) / float(process_get))
                hit_rank = float(hit_rank) * 100
                hit_rank = "%.0f" % hit_rank
            nowtime = int(time.time())
            log = Logs(num=hit_rank,get=process_get,hit=process_hit,log_type=1,time=nowtime,m_id=mid)
            db_session.add(log)
            db_session.commit()
            this_data = str(current_get) + ' ' + str(current_hit)
            fw = open(log_file,'w')
            fw.write(this_data)
            fw.close()
    except Exception, e :
        continue
