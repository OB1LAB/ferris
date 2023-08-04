from flask_restful import Resource
from my_libs.config import Config


class InfoApi(Resource):
    def get(self):
        return Config.info_server
