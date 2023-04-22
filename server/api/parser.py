from flask import request
from flask_restful import Resource
from my_libs.logs import Logs


class Parser(Resource):
    def get(self):
        args = request.args
        return logs_parser.parser(int(args['offset']))

    def post(self):
        data = request.get_json()
        return logs_parser.send_msg(data['msg'])


logs_parser = Logs()
