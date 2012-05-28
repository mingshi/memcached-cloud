# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from mc.model import *
from mc.db.db import db_session

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    return render_template("mc/index.html", server_count = db_session.query(Memcacheds).count())

