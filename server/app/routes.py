from app import api
from api.activity import ActivityPlayersApi
from api.staff import StaffApi
from api.parser import ParserApi
from api.finder import FinderApi
from api.logs import LogsApi
from api.info import InfoApi

api.add_resource(ActivityPlayersApi, '/api/getActivity')
api.add_resource(StaffApi, '/api/getStaff')
api.add_resource(ParserApi, '/api/parser')
api.add_resource(FinderApi, '/api/finder')
api.add_resource(LogsApi, '/api/logs')
api.add_resource(InfoApi, '/api/info')
