from app import api
from api.activity import ActivityPlayers
from api.staff import Staff
from api.parser import Parser

api.add_resource(ActivityPlayers, '/api/getActivity')
api.add_resource(Staff, '/api/getStaff')
api.add_resource(Parser, '/api/parser')
