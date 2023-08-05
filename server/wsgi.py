import gevent.monkey; gevent.monkey.patch_all()
from app import app, socketio
from my_libs.config import Config
from engineio.async_drivers import gevent

if __name__ == '__main__':
    port = 8000
    config = Config()
    config.create_files()
    print(f'Server start on localhost:{port}')
    socketio.run(app, host='0.0.0.0', port=8000)
