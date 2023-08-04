from flask import request
from flask_restful import Resource
from my_libs.minecraft_activity import get_activity


class ActivityPlayersApi(Resource):
    def post(self):
        data = request.get_json()
        return get_activity(data['first_date'], data['second_date'], data['players'], data['server'])
