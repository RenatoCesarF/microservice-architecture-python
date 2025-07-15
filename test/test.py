from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

# Conectando no MongoDB local
client = MongoClient("mongodb://localhost:27018")
db = client["mp3s"]

# Usando GridFS
fs = gridfs.GridFS(db)

# Buscando o vídeo pelo ObjectId
video = fs.get(ObjectId("6875bbff5b2c97d017510114"))

# Salvando localmente para validar
with open("video_debug.mp3", "wb") as f:
    f.write(video.read())
