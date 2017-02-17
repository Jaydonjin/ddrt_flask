"""deimos entry point

"""
import gevent.monkey

gevent.monkey.patch_all()

if __name__ == '__main__':
    import os

    from gevent.wsgi import WSGIServer
    from app import create_app

    ENV_NAME = 'ENV'

    app = create_app(os.environ.get(ENV_NAME, 'development'))

    app.logger.info('demo listening %s:%s', app.config['HTTP_HOST'], app.config['HTTP_PORT'])

    if app.config.get('DEBUG', False):
        app.run(app.config['HTTP_HOST'], app.config['HTTP_PORT'], debug=False)
    else:
        WSGIServer((app.config['HTTP_HOST'], app.config['HTTP_PORT']), application=app,
                   log=None).serve_forever()
