from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///token.sqlite3"

db = SQLAlchemy(app)

class pin_table(db.Model):
    id = db.Column('id',db.Integer,primary_key = True)
    pin = db.Column(db.String(15),unique=True,nullable=False)
    def __init__(self,pin):
        self.pin = pin