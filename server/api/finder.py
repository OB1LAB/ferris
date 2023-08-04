from flask import request
from flask_restful import Resource
from my_libs.logs_finder import global_find


class FinderApi(Resource):
    def post(self):
        data = request.get_json()
        return global_find(data['first_date'], data['second_date'],
                           data['findData'], data['server'])
