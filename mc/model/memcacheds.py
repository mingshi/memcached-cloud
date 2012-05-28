# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from mc.db.db import Model

class Memcacheds(Model):
    """
    memcacheds model
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    port = Column(Integer)
    group_id = Column(Integer, ForeignKey('groups.id'))
    parameters = Column(String(255))
    status = Column(Integer)

    def __init__(self, ip, port, group_id, status, parameters = ''):
        """
        constructor of Memcacheds class

        ip: server ip
        port: server port
        ground_id: group id
        status: status of memcached. 0..stopped 1..running
        """
        self.ip = ip
        self.port = port
        self.group_id = group_id
        self.status = status

    def __repr__(self):
        return '<Memcached %r' % (self.ip + ":" + str(self.port))

