from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy
import uuid
from twilio.rest import Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///main.db'
db = SQLAlchemy(app)


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
def process_data(json_blob):
    police_called = call_police()
    data = json.loads(json_blob)
    if data["uuid"] is None:
        data["uuid"] = uuid.uuid4()
    # Process timestamp data
    try:
        if data["message_type"] == "Audio":
            db.session.add(Audio(**data))
        elif data["message_type"] == "Metadata":
            db.session.add(Metadata(**data))
    except:
        return_packet = {"police_called": police_called,
                         "success": False}
    else:
        return_packet = {
            "uuid": data["uuid"],
            "success": True
        }
    return json.dumps(return_packet)


def call_police():
    account_sid = "AC5ea2cdc4f220cd56dd5ef910fda8b6d5"
    auth_token = "825cce384001f5b8b469ea5c4e6ef8ed"
    client = Client(account_sid, auth_token)

    # Start a phone call
    call = client.calls.create(
        to="+12019034616",
        from_="+19145899232",
        url="https://raw.githubusercontent.com/samsontmr/cerberus-rex/master/"
            "emergency_call.xml?token=AQdayG-57_wu_gg7x1SOf5tRj0KCzfq-ks5akk"
            "vDwA%3D%3D"
    )

    return True


@app.route('/')
def process_audio():
    return "bananas\n", 500
