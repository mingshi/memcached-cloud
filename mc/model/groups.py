# -*- coding: utf-8 -*-
from mc.db.db import Model
from sqlalchemy import Column, Integer, String

class Groups(Model):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    #memcacheds = relationship('Memcacheds', backref='groups', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.name

