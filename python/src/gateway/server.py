import  gridfs, pika, json
import logging

from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from auth_service import access
from auth import validate
from storage import util
from utils.logger import setup_logger


server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://mongo:27017/videos"

mongo_videos = PyMongo(server, uri="mongodb://mongo:27017/videos")
mongo_mp3s = PyMongo(server, uri="mongodb://mongo:27017/mp3s")

logging.basicConfig(level=logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.WARNING)

logger = setup_logger("app")


if mongo_videos.db is None:
    raise Exception(f"Mongo is None: {mongo_videos.db}")

if mongo_mp3s.db is None:
    raise Exception(f"Mongo is None: {mongo_mp3s.db}")

# mongo.db.list_collections()
fs_videos = gridfs.GridFS(mongo_videos.db)
fs_mp3s = gridfs.GridFS(mongo_mp3s.db)


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
        err = util.upload(f, fs_videos, channel, access)

        if err:
            return err
    
    return "Success", 200


@server.route("/download", methods=["GET"])
def download(): 
    access, err = validate.token(request)

    if err is not None:
        return err

    if access is None:
        return "access invalid", 403

    access = json.loads(access)

    if not access["admin"]:
        return "not authorized", 403


    fid_string = request.args.get("fid")

    if not fid_string:
        return "fid not received", 400


    try: 
        out = fs_mp3s.get(ObjectId(fid_string))
        download_name = f"{fid_string}.mp3"
        return send_file(out, download_name=download_name), 200

    except Exception as err:
        logger.error(err)
        return "internal server error", 500

if __name__ == "__main__":
    server.logger.info("Running on 8080")
    server.run(host="0.0.0.0", port=8080, debug=True)


