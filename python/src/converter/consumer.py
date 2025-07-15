import pika, sys, os
import logging

from pymongo import MongoClient
import gridfs
from convert import to_mp3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def main():
    client = MongoClient("mongo", 27017 )

    db_videos = client.videos
    db_mp3s = client.mp3s

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )

    def callback(channel, method, properties, body):
        logging.info(f"Received message\nbody:{body}")
        err = to_mp3.start(body, fs_videos, fs_mp3s, channel)
        if err:
            logging.error(f"Error on callback: {err}")
            channel.basic_nack(delivery_tag=method.delivery_tag)
            return
        
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel = connection.channel()

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=callback
    )

    logging.info("--- Waiting for messages ----")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        logging.info("Running main")
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    # except Exception as err:
    #     logging.info("Error on main:\n")
    #     logging.error(err)





