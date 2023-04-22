from flask_restful import Resource
from my_libs.OB1L1B import get_staff


class Staff(Resource):
    def get(self):
        return staff


staff = get_staff()
