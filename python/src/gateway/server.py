import  gridfs, pika, json

from flask import Flask, request
from flask_pymongo import PyMongo
import logging

from auth_service import access
from auth import validate
from storage import util
from utils.logger import setup_logger


server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://mongo:27017/videos"

logging.basicConfig(level=logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.WARNING)

logger = setup_logger("app")

mongo = PyMongo(server)

if mongo.db is None:
    raise Exception(f"Mongo is None: {mongo.db}")

mongo.db.list_collections()
fs = gridfs.GridFS(mongo.db)


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if err:
        return err

    if not token:
        return "unknow error", 500

    return token, 200

@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err is not None:
        return err

    if access is None:
        return "access invalid", 403

    access = json.loads(access)

    if not access["admin"]:
        return "not authorized", 200

    if len(request.files) > 1 or len(request.files) < 1:
        return "exactly 1 file required", 400

    for _, f in request.files.items():
        err = util.upload(f, fs, channel, access)

        if err:
            return err
    
    return "Success", 200


@server.route("/download", methods=["GET"])
def download(): 
    return "", 200

if __name__ == "__main__":
    server.logger.info("Running on 8080")
    server.run(host="0.0.0.0", port=8080, debug=True)


