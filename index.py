from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os.path
import uuid
from twilio.rest import Client
import folium
from folium.plugins import fast_marker_cluster
import random
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "build")


class Metadata(db.Model):
    id = db.Column(db.String, primary_key=True)
    message_type = db.Column(db.String, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=True)
    longitude = db.Column(db.Float, unique=False, nullable=True)
    loc_accuracy = db.Column(db.Integer, unique=False, nullable=True)
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

def generate_random_data(lat, lon, n_samples, n_centers):
    centers = np.zeros((n_centers, 2))
    for i in range(n_centers - 1):
        dec_lat = (random.random() * 2 - 1) / 100
        dec_lon = (random.random() * 2 - 1) / 100
        centers[i][0] = 37.427829 + dec_lat
        centers[i][1] = -122.170214 + dec_lon
        centers[-1][0] = lat
        centers[-1][1] = lon

    data, cluster_labels = make_blobs(n_samples=n_samples, centers=centers,
                                      cluster_std=0.0004, random_state=0)
    return data, cluster_labels


def generate_map():
    m = folium.Map(location=[37.427829, -122.170214], zoom_start=13)
    fast_cluster = fast_marker_cluster([]).add_to(m)

    folium.Marker(
        location=[45.3300, -121.6823],
        popup='USER{}'.format(Metadata.id),
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    m.save('index.html')


@app.route('/new_message', methods=["POST"])
def process_data():
    data = request.get_json()
    print(data)
    police_called = call_police()
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
            "police_called": police_called,
            "success": True
        }
    return return_packet


def call_police():
    account_sid = "AC5ea2cdc4f220cd56dd5ef910fda8b6d5"
    auth_token = "825cce384001f5b8b469ea5c4e6ef8ed"
    try:
        client = Client(account_sid, auth_token)
        # Start a phone call
        call = client.calls.create(
            to="+19145899232",
            from_="+12019034616",
            url="https://www.adamcircle.com/emergency_call.xml"
        )
    except:
        return False
    else:
        return True
