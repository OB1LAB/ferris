from flask import request
from flask_restful import Resource
from my_libs.minecraftActivity import get_activity


class ActivityPlayers(Resource):
    def post(self):
        data = request.get_json()
        return get_activity(data['first_date'], data['second_date'], data['players'])
