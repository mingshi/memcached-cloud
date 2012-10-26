# -*- coding: utf-8 -*-
from mc.db.db import Model
from sqlalchemy import Column, Integer, String

class Logs(Model) :
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    num = Column(Integer)
    get = Column(Integer)
    hit = Column(Integer)
    log_type = Column(Integer)
    time = Column(Integer, unique=True)
    m_id = Column(Integer, index=True)

    def __init__(self, num, get, hit, log_type, time, m_id):
        self.num = num
        self.get = get
        self.hit = hit
        self.log_type = log_type
        self.time = time
        self.m_id = m_id
