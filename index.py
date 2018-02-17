from flask import Flask


app = Flask(__name__)

@app.route('/new', method="POST")
def process_location_data(json_blob):
    timestamp
    userid
    lat
    lon
    shooter_nearby
    injury
    return