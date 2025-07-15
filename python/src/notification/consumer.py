
import pika, sys, os
import logging

from send import email


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )

    def callback(channel, method, properties, body):
        logging.info(f"Received message\nbody:{body}")
        err = email.notification(body)
        if err:
            logging.error(f"Error on callback: {err}")
            channel.basic_nack(delivery_tag=method.delivery_tag)
            return
        
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel = connection.channel()

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
        on_message_callback=callback
    )

    logging.info("--- Waiting for messages in mp3 queue ----")

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





