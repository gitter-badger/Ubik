import config
from flask import Flask, request
import json
import os
import requests
import modules
from utils.log import *
from db import Database
from modules.src.question import Question
from modules.src.answer import Answer
from modules.src.user import User

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', config.VERIFY_TOKEN)
DATABASE_NAME = os.environ.get('DATABASE_NAME', config.DATABASE_NAME)
DATABASE_USER = os.environ.get('DATABASE_USER', config.DATABASE_USER)
DATABASE_PASS = os.environ.get('DATABASE_PASS', config.DATABASE_PASS)

app = Flask(__name__)
db = Database(DATABASE_NAME, DATABASE_USER, DATABASE_PASS)
question_handler = Question(db)
answer_handler = Answer(db)
user_handler = User(db)


@app.route('/')
def info():
    return "Hi! I am Ubik. I will get the best people to answer your questions." \
        " Ask anything sensible. Also please don't include any personal details." \
        " This is an anonymous Q&A platform, built on confidence. " \
        "If you ask indecent questions, you will lose right to ask. " \
        "Similar rules apply for those who answer questions. But don't worry, I am there for you." \
         " Ohh! I forgot to tell you, I rose from dead."

@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json(force=True)
        log(data)  # you may not want to log every incoming message in production, but it's good for testing

        if data["object"] == "page":

            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        handle_message(message_text, sender_id)
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

        return "ok", 200

    elif request.method == 'GET':  # Verification
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        else:
            return 'Error, wrong validation token', 403

def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
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

def handle_message(message_text, sender_id):
    if message_text.startswith('[Question]'):
        question_handler.add_question(message_text, sender_id)
        response_text = question_handler.fetch_response()
    elif message_text.startswith('[Answer]'):
        answer_handler.add_answer(message_text, sender_id)
        response_text = answer_handler.fetch_response()
    else:
        response_text = "Hi, I am Ubik. You can ask me your question."
    send_message(sender_id, response_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
