# -*- coding: utf-8 -*-
import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV="Development"

class Config(object):
    HOST='0.0.0.0'
    PORT=8818
    DB_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    PORT=3000
    DEBUG=True
    DB_URI="mysql://mc:mc@192.168.1.59/mc"

