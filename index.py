from flask import Flask
import json
from pymongo import MongoClient


app = Flask(__name__)

@app.route('/new', method="POST")
def process_location_data(json_blob):
    deciphered = json.loads(json_blob)
    write_to_mongo(deciphered)


def write_to_mongo(data):
    cli = MongoClient()
    db = cli.pymongo_test
    posts = db.posts
    posts.insert_one(data)


def read_from_mongo():
    pass