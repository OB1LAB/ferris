import requests
from flask import Flask, Response
from config import Config
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

version = '1.08'
app = Flask(__name__, static_folder=None)
app.config.from_object(Config)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    response = requests.get(f'https://ob1lab.ru/api/FrontendDesktop?version={version}&file_name=index.html')
    return Response(response.content, mimetype='text/html')


@app.route('/favicon.ico')
def favicon():
    response = requests.get(f'https://ob1lab.ru/api/FrontendDesktop?version={version}&file_name=favicon.ico')
    return Response(response.content, mimetype='image/x-icon')


@app.route('/assets/<filename>')
def assets(filename):
    response = requests.get(f'https://ob1lab.ru/api/FrontendDesktop?version={version}&file_name={filename}')
    if filename.split('.')[1] == 'js':
        type_file = 'application/javascript'
    elif filename.split('.')[1] == 'css':
        type_file = 'text/css'
    elif filename.split('.')[1] == 'woff':
        type_file = 'application/font-woff'
    elif filename.split('.')[1] == 'woff2':
        type_file = 'application/font/woff2'
    elif filename.split('.')[1] == 'ttf':
        type_file = 'application/font-ttf'
    elif filename.split('.')[1] == 'eot':
        type_file = 'application/vnd.ms-fontobject'
    return Response(response.content, mimetype=type_file)


@app.errorhandler(404)
def page_not_found(e):
    response = requests.get(f'https://ob1lab.ru/api/FrontendDesktop?version={version}&file_name=index.html')
    return Response(response.content, mimetype='text/html')

from app import routes
