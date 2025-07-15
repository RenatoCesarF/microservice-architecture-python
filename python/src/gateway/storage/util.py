import pika, json
from pika.adapters.blocking_connection import BlockingChannel

from utils.logger import setup_logger

logger = setup_logger("app")

def upload(f, fs, channel: BlockingChannel, access):
    try:
        pos = f.tell()
        f.seek(0, 2)
        size = f.tell()
        f.seek(pos)

        logger.debug(f"[DEBUG] Tamanho do arquivo recebido: {size} bytes")
        fid = fs.put(f)
    except Exception as err:
        logger.error(f"Error ao salvar video:\n {err}")
        return "internal server error ", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                    delivery_mode=2
                )
        )
    except Exception as err:
        logger.error(f"Error on publishing: {err}")
        fs.delete(fid)
        return "internal server error", 500



