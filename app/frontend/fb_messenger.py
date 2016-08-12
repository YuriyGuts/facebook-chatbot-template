import json
import os
import logging
import logging.config
import ssl
import sys

import requests

# Add parent dir to PYTHONPATH to make imports more convenient.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from conversation import responder
from flask import Flask, request


app = Flask(__name__)
logger = logging.getLogger(__name__)

security_tokens = {
    "fb_page_access_token": os.environ["FB_PAGE_ACCESS_TOKEN"],
    "fb_webhook_verify_token": os.environ["FB_WEBHOOK_VERIFY_TOKEN"],
}

ssl_certs = {
    "certificate_file": os.environ["SSL_CERTIFICATE_FILE"],
    "private_key_file": os.environ["SSL_PRIVATE_KEY_FILE"],
}


@app.route('/', methods=['GET'])
def verify_webhook():
    # When the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments.
    correct_token = security_tokens["fb_webhook_verify_token"]
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == correct_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Ready to talk!", 200


@app.route('/', methods=['POST'])
def webhook():
    # Endpoint for processing incoming messaging events.
    data = request.get_json()

    # We may not want to log every incoming message in production, but it's good for testing.
    logging.info(data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                process_messaging_event(messaging_event)

    return "ok", 200


def process_messaging_event(event):
    # Someone sent our page a message.
    if event.get("message"):
        process_incoming_message_event(event)

    # Delivery confirmation.
    if event.get("delivery"):
        pass

    # Opt-in confirmation.
    if event.get("optin"):
        pass

    # User clicked/tapped "postback" button in an earlier message.
    if event.get("postback"):
        pass


def process_incoming_message_event(event):
    sender_id = event["sender"]["id"]
    send_begin_typing_event(sender_id)
    text, attachment = responder.get_reply(event)

    # Facebook Messenger doesn't allow plain text messages longer than 320 characters.
    if text is not None and len(text) > 320:
        text = text[:310] + "..(cut).."

    send_reply(sender_id, text, attachment)


def send_reply(recipient_id, message_text, message_attachment):
    logger.info("Sending message to {recipient_id}: {message_text}".format(**locals()))

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    if message_attachment is not None:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": json.dumps(message_attachment)
            }
        })

    send_facebook_message_payload(data)


def send_begin_typing_event(recipient_id):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
    })
    send_facebook_message_payload(data)


def send_end_typing_event(recipient_id):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_off"
    })
    send_facebook_message_payload(data)


def send_facebook_message_payload(data):
    params = {
        "access_token": security_tokens["fb_page_access_token"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    reply_request = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        headers=headers,
        data=data
    )

    if reply_request.status_code != 200:
        logger.error("{reply_request.status_code}: {reply_request.text}".format(**locals()))


def setup_logging(config_filename="logging.json", default_level=logging.INFO):
    """Configure logging handlers and levels."""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    if os.path.exists(config_filename):
        with open(config_filename, 'rt') as config_file:
            logging_config = json.load(config_file)
        logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(level=default_level)


def create_ssl_context():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.load_cert_chain(certfile=ssl_certs["certificate_file"], keyfile=ssl_certs["private_key_file"])
    return ssl_context


if __name__ == "__main__":
    setup_logging()
    ssl_context = create_ssl_context()
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=ssl_context)
