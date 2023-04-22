from flask import Flask
from config import Config
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
CORS(app, supports_credentials=True)

from app import routes
