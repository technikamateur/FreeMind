from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from FreeMind import config
import os

# Boilerplate
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from FreeMind import commands, models, api
