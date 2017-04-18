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
    Sends the messaged_text to recipient with given recipient_id

    :param recipient_id: unique facebook id of the user, to whom the message is to be sent.
    :param message_text: The message to be sent to the recipient.
    :return: None
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
    Post a quick reply for askers to rate the users for answers they got.

    :param asker_id: unique facebook id of the asker.
    :param responder_id: unique facebook id of the person qho answered asker's question.
    :return: None
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
    """
    Checks if the string (s) has any non-askii character.

    :param s: The string which is checked
    :return: True, is the string consists of all ascii characters, else returns False.
    """
    return all(ord(c) < 128 for c in s)
