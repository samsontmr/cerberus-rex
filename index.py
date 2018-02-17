from flask import Flask
import json
from pymongo import MongoClient


app = Flask(__name__)

@app.route('/new', method="POST")
def process_location_data(json_blob):
    deciphered = json.dump(json_blob)
    return deciphered

def write_to_mongo(data):
    cli = MongoClient()
    db = cli.pymongo_test
    posts = db.posts
    posts.insert_one(json.loads(data))