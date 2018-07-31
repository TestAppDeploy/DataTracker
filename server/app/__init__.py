# ini file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='../static/dist', template_folder='../static/client')
db = SQLAlchemy(app)

from .config import Config

app.config.from_object(Config)

migrate = Migrate(app, db)


from .server import models
