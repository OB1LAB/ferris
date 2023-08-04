from app import app, socketio
from my_libs.config import Config

if __name__ == '__main__':
    config = Config()
    config.create_files()
    socketio.run(app, host='0.0.0.0', port=8000)
