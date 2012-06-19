# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for

mod = Blueprint("help", __name__, url_prefix="/helps")

@mod.route('/')
def help():
    #return redirect(url_for(".help_quick_start"))
    return render_template("mc/help/index.html")

@mod.route('/quick-start')
def help_quick_start():
    return render_template("mc/help/quick_start.html")

