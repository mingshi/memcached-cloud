# -*- coding: utf-8 -*-
from mc.db.db import Model

class Groups(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    memcacheds = db.relationship('Memcacheds', backref='groups', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.name

