from flask import request
from flask_restful import Resource
from threading import Lock
from app import socketio
import platform


class ParserApi(Resource):
    def get(self):
        return logs_parser.get_data()

    def post(self):
        data = request.get_json()
        return logs_parser.send_msg(data['msg'])


if platform.system() == 'Windows':
    from my_libs.logs_interact_windows import Logs
else:
    from my_libs.logs_interact_other import Logs
logs_parser = Logs()
thread_lock = Lock()
with thread_lock:
    socketio.start_background_task(target=logs_parser.parser)
count_connection = 0


@socketio.on('connect')
def handle_connect():
    global count_connection
    if not count_connection:
        logs_parser.run = True
    count_connection += 1


@socketio.on('disconnect')
def handle_disconnect():
    global count_connection
    count_connection -= 1
    if not count_connection:
        logs_parser.run = False
