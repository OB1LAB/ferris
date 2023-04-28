from flask import request
from flask_restful import Resource
import platform


class Parser(Resource):
    def get(self):
        args = request.args
        return logs_parser.parser(int(args['offset']))

    def post(self):
        data = request.get_json()
        return logs_parser.send_msg(data['msg'])


if platform.system() == 'Windows':
    from my_libs.logs_interact_windows import Logs
else:
    from my_libs.logs_interact_other import Logs
logs_parser = Logs()
