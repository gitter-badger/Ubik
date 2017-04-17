import os
import json
import requests
import config
from utils.log import log


ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
params = {
    "access_token": ACCESS_TOKEN
}
headers = {
    "Content-Type": "application/json"
}

def send_message(recipient_id, message_text):
    """

    :param recipient_id:
    :param message_text:
    :return:
    """
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def get_feedback(asker_id, responder_id, question):
    """

    :param recipient_id:
    :return:
    """
    log("sending feedback callback message to {recipient}".format(recipient=asker_id))

    data = json.dumps({
        "recipient": {
            "id": asker_id
        },
        "message":{
            "text": "Rate the answer: (Marking OOW(Out of World), means you are satisfied, and don't want any more answers)",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Vulgar",
                    "payload": "{0}, {1}, {2}, {3}".format(-20, 'Vulgar', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "Unrelated",
                    "payload": "{0}, {1}, {2}, {3}".format(-5, 'Unrelated', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "Bad",
                    "payload": "{0}, {1}, {2}, {3}".format(-10, 'Bad', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "Average",
                    "payload": "{0}, {1}, {2}, {3}".format(+1, 'Average', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "Good",
                    "payload": "{0}, {1}, {2}, {3}".format(+10, 'Good', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "Best",
                    "payload": "{0}, {1}, {2}, {3}".format(+20, 'Best', responder_id, question),
                },
                {
                    "content_type": "text",
                    "title": "OOW",
                    "payload": "{0}, {1}, {2}, {3}".format(+100, 'OOW', responder_id, question),
                }
            ]
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)
