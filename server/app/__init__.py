from flask import Flask, send_file
from config import Config
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__, static_url_path='/assets', static_folder='../static/assets')
app.config.from_object(Config)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return send_file('../static/index.html')

@app.route('/favicon.ico')
def favicon():
    return send_file('../static/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return send_file('../static/index.html')

from app import routes
