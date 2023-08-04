from flask_restful import Resource
from my_libs.config import Config


class StaffApi(Resource):
    def get(self):
        return Config.staff
