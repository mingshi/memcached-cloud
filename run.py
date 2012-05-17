if __name__ == "__main__":
#    from mc import app
#
#    if app.config['DEBUG'] :
#        print app.config
#
#    app.run(host=app.config['HOST'], port=app.config['PORT'])

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from mc import app

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
