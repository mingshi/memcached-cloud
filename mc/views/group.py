from flask import Blueprint, render_template, request
from mc.db.db import db_session
from mc.model import *

mod = Blueprint("group", __name__)

@mod.route('/groups')
def groups_index():
    from sqlalchemy import func
    groups = db_session.query(Groups).all()
    
    return  render_template('mc/groups_index.html', groups = groups)












