import json
import logging

from conversation import intent


logger = logging.getLogger(__name__)


def get_reply(event):
    sender_id = event["sender"]["id"]
    message_text = event["message"]["text"]
    interpretation = intent.parse_intent(sender_id, message_text)
    print("Interpretation:", interpretation)

    default_response_text = "Sorry, can't understand that." \
        + "\n\nInterpretation:\n" \
        + json.dumps(interpretation)

    text = default_response_text
    attachment = None

    if interpretation is not None and "msg" in interpretation:
        suggested_response_text = interpretation["msg"]["msg"]
        text = suggested_response_text
        attachment = None

    try:
        intent_name, entities = extract_intent_parameters(interpretation)

        # ------------------------------
        # Add your custom intents here.
        # ------------------------------
        if intent_name == "HelloWorldIntent":
            text, attachment = reply_to_hello_world_intent(entities)

    except:
        text = default_response_text
        attachment = None

    return text, attachment


def extract_intent_parameters(interpretation):
    if interpretation is not None:
        if "action" in interpretation and "entities" in interpretation["action"]:
            entities = interpretation["action"]["entities"]
            if "intent" in entities:
                intent_name = entities["intent"][0]["value"]
                return intent_name, entities

    return None, None


def reply_to_hello_world_intent(entities):
    text = None
    attachment = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": "Hello World",
                    "subtitle": "Sample chat bot response",
                    "buttons": [{
                        "type": "web_url",
                        "url": "https://github.com/YuriyGuts/facebook-chatbot-template",
                        "title": "Go to GitHub"
                    }]
                }
            ]
        }
    }
    return text, attachment
