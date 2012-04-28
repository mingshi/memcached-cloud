if __name__ == "__main__":
    from mc import app

    if app.config['DEBUG'] :
        print app.config

    app.run(host=app.config['HOST'], port=app.config['PORT'])
