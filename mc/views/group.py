from flask import Blueprint, render_template, request
from mc.db.db import db_session
from mc.model import *
import json

mod = Blueprint("group", __name__)

@mod.route('/groups')
def groups_index():
    from sqlalchemy import func
    groups = db_session.query(Groups).all()
    
    return  render_template('mc/groups_index.html', groups = groups)

@mod.route('/group-add')
def group_add():
    
    return  render_template('mc/group_add.html')

@mod.route('/group/do_add', methods=['GET','POST'])
def group_do_add() :
    result = {}

    if not request.form.has_key('name') :
        result['status'] = 'error'
        result['message'] = 'please input name'
    else :
        name = request.form['name']
        count = db_session.query(Groups).filter_by(name = name).count()
        if (count > 0) :
            result['status'] = 'error'
            result['message'] = 'group ' + name + ' is existed!'
        else :
            group = Groups(name)
            db_session.add(group)
            db_session.commit()
            result['status'] = 'ok'
            result['message'] = 'add successed. group id is ' + str(group.id)

    return json.dumps(result)

