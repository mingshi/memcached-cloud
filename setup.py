from setuptools import setup

setup (
    name='mc',
    install_requires=[
        'python-memcached',
        'Flask',
        'sqlalchemy',
        'Flask-SQLAlchemy',
        'oursql',
    ]
)

