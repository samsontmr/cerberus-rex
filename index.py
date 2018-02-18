from flask import Flask, request, send_from_directory, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import os.path
import uuid
from twilio.rest import Client


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///main.db'
db = SQLAlchemy(app)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "build")

class Metadata(db.Model):
    id = db.Column(db.String, primary_key=True)
    message_type = db.Column(db.String, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=True)
    longitude = db.Column(db.Float, unique=False, nullable=True)
    shooter_nearby = db.Column(db.Boolean, unique=False, nullable=True)
    medical_requested = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Metadata-ID: %r>' % self.id


class Audio(db.Model):
    id = db.Column(db.String, primary_key=True)
    message_type = db.Column(db.String, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    audio = db.Column(db.BLOB, unique=False, nullable=True)

    def __repr__(self):
        return '<Audio-ID: %r>' % self.id


db.create_all()





@app.route('/new_message', methods=["POST"])
def process_data():
    data = request.get_json()
    print(data)
    #police_called = call_police()
    if data["uuid"] is None:
        data["uuid"] = uuid.uuid4()
    # Process timestamp data
        try:
            if data["message_type"] == "Audio":
                db.session.add(Audio(**data))
            elif data["message_type"] == "Metadata":
                db.session.add(Metadata(**data))
        except:
            return_packet = {"police_called": True,
                         "success": False,
                         "uuid": data["uuid"]}
    else:
        return_packet = {
            "uuid": data["uuid"],
            "success": True
        }

    response = app.response_class(
        response=json.dumps(return_packet),
        status=200,
        mimetype='application/json'
    )
    return response


def call_police():
    account_sid = "AC5ea2cdc4f220cd56dd5ef910fda8b6d5"
    auth_token = "825cce384001f5b8b469ea5c4e6ef8ed"
    client = Client(account_sid, auth_token)

    # Start a phone call
    call = client.calls.create(
        to="+19145899232",
        from_="+12019034616",
        url="https://www.adamcircle.com/emergency_call.xml"
    )

    return True


@app.route('/')
def process_audio():
    return "bananas\n", 500
