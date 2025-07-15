import logging
import smtplib, os, json

from email.message import EmailMessage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_addres = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")

        assert sender_addres
        assert sender_password

        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_addres
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        # session.ehlo()
        session.login(sender_addres, sender_password)
        session.send_message(msg, sender_addres, receiver_address)
        session.quit()
        logging.info("Mail sent")
    except Exception as err: 
        logging.error(err)
        return err
