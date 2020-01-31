import os
import uuid,base64
from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import random
from flask_uuid import FlaskUUID

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "sqlite:///token.sqlite3"
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

class pin_table(db.Model):
    id = db.Column('id',db.Integer,primary_key = True)
    pin = db.Column(db.String(15),unique=True,nullable=False)
    def __init__(self,pin):
        self.pin = pin


class Generate(Resource):
    def get(self):
        db.session.add(pin_table(str(int(uuid.uuid4()))[:15]))
        db.session.commit()
        all = pin_table.query.all()
        result = pin_table.query.filter_by(id = len(all)).first()
        id = result.id
        pin = result.pin
        return jsonify({'id':id,"pin":pin})

api.add_resource(Generate, '/')

class validate(Resource):
    def get(self):
        request_data = request.get_json()
        id = request_data['id']
        pin = request_data['pin']
        if pin_table.query.filter_by(pin= str(pin)).first() is not None:
            return "1"
        else:
            return "0"


api.add_resource(validate, '/valid')


if __name__ == '__main__':
    app.run()

