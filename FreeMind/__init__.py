import FreeMind.config as config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Boilerplate
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

import FreeMind.models
db.create_all()

import FreeMind.commands, FreeMind.api, FreeMind.action, FreeMind.logger, FreeMind.views
import FreeMind.action.actions as actions, FreeMind.action.properties as properties
from FreeMind.plugins.momentjs import momentjs

app.jinja_env.globals['momentjs'] = momentjs
