# -*- coding: utf-8 -*-
import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV="Development"

class Config(object):
    HOST='0.0.0.0'
    PORT=8818

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    PORT=3000
    DEBUG=True


