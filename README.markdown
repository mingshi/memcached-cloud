# Memcache-Cloud

## get your python

we recommend using isolated python enviroment, using `pythonbrew`. you can find it [here](https://github.com/utahta/pythonbrew). through the following commands, you are good to go.

install `pythonbrew`.

```
$ curl -kL http://xrl.us/pythonbrewinstall | bash
```

add this to your `~/.bashrc`.

```
[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc
```

after that, reload your shell env and install the required python version.

```
$ source /etc/profile
$ pythonbrew install 2.7.3
```

# How to start?

## setuptools or pip ?
make sure you have `easy_install` or `pip` installed. in the most case if you use `pythonbrew`, they're already installed. Or you can install by yourself.

```
$ apt-get install python-setuptools
$ apt-get install python-pip
```

## solve the projects dependencies.

run following command to install the project dependencies.

```
$ python setup.py install
```

## show me the config

memcache-cloud using different config for different enviroment such as `production` and `development`. here is how it works

+ a file named `env.py` with content like `ENV="ProductionConfig"` specified the enviroment.
+ memcache-cloud judging from a config named 'ENV' to load the according config from a file named `config.py` in the root directory of the project.

    ```
    ENV="Development"

    class Config(object):
        HOST='0.0.0.0'
        PORT=8818

    class ProductionConfig(Config):
        DEBUG=False

    class DevelopmentConfig(Config):
        PORT=3000
        DEBUG=True
    ```

## setup a database for playing around

1. config database in env.py.

    ```
    class DevelopmentConfig(Config):
        PORT=3000
        DEBUG=True
        DB_URI="mysql+oursql://mc:mc@localhost/mc"
    ```

2.run the initdb.py

    ```
    $ python initdb.py
    ```

## enjoy it!
