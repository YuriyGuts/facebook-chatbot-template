import json
import logging
import os
import requests


logger = logging.getLogger(__name__)


def parse_intent(sender_id, message_text):
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {token}".format(token=os.environ["WIT_AI_SERVER_TOKEN"]),
    }
    query_string_params = {
        "v": "20160721",
        "session_id": str(sender_id),   # TODO: generate a separate session_id per conversation.
        "q": message_text
    }
    endpoint = "https://api.wit.ai/converse"

    # We need to call "/converse" consecutively until we reach the "stop" message.
    # After every call, the service will give us a new piece of information (intent, suggested reply, etc.).
    responses = {}
    while True:
        logger.info("Querying wit.ai")
        response = requests.post(endpoint, headers=headers, params=query_string_params)
        logger.info("wit.ai response code: {0}".format(response.status_code))

        # After the first call, we no longer need the message to be passed in the request.
        # Otherwise, we'll enter an infinite loop.
        if "q" in query_string_params:
            del query_string_params["q"]

        if response.status_code != requests.codes.ok:
            break

        response_data = json.loads(response.text)
        if response_data["type"] == "stop":
            break

        # Accumulate all response types retrieved from the service.
        responses[response_data["type"]] = response_data

    return responses
