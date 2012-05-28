#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mc.db.db import init_db, db_session

if __name__ == "__main__":
    print "bwgin inited db \n"
    init_db()

    from mc.model.memcacheds import Memcacheds

    #memcache = Memcacheds(ip='192.168.1.96', port=11212, status=1, group_id =1,version='1.4.0')
    #db_session.add(memcache)
    #db_session.commit()
    
    print "inited db end \n"


