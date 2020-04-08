from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/mainsana'
app.environment = "development"
app.debug = True

db = SQLAlchemy(app)
json = FlaskJSON(app)