import pika, json, tempfile, os
from bson.objectid import ObjectId
from moviepy.video.io.VideoFileClip import VideoFileClip

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def start(message, fs_videos, fs_mp3s, channel):
    # try:
    message = json.loads(message)
    # except Exception as e:
    #     logging.error(f"invalid JSON: {e}")
    #     return "invalid message format"

    tf = tempfile.NamedTemporaryFile(delete=False)  # manter arquivo no disco mesmo após fechar
    out = fs_videos.get(ObjectId(message["video_fid"]))
    tf.write(out.read())

    audio = VideoFileClip(tf.name).audio

    tf.flush()
    tf.close()

    if audio is None:
        print("[ERROR] video has no audio")
        return "video has no audio to export"

    file_name = message["video_fid"]
    tf_path = os.path.join(tempfile.gettempdir(), f"{file_name}.mp3")
    audio.write_audiofile(tf_path)

    with open(tf_path, "rb") as f:
        data = f.read()
        fid = fs_mp3s.put(data)
        f.close()

    os.remove(tf_path)
    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        )
    except Exception as err:
        logging.error(err)
        fs_mp3s.delete(fid)
        return "unable do publish message"

    logging.info(f"Finished ID: {message['video_fid']} ")
