import os
import uuid,base64
from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
import random
from flask_uuid import FlaskUUID
from flask_sqlalchemy import SQLAlchemy
from connect import pin_table


app = Flask(__name__)

api = Api(app)

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "sqlite:///token.sqlite3"
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Generate(Resource):
    def get(self):
        db.session.add(pin_table(str(int(uuid.uuid4()))[:15]))
        db.session.commit()
        all = pin_table.query.all()
        result = pin_table.query.filter_by(id = len(all)).first()
        id = result.id
        pin = result.pin
        return {'id':id,"pin":pin}

class validate(Resource):
    def get(self):
        request_data = request.get_json()
        id = request_data['id']
        pin = request_data['pin']
        if pin_table.query.filter_by(pin= str(pin)).first() is not None:
            return "1"
        else:
            return "0"


api.add_resource(validate, '/valid_token')
api.add_resource(Generate, '/token')

app.run(port = 5000, debug=True)

