"""
MIT License

Copyright (c) 2017 Harshal Priyadarshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import config
from flask import Flask, request
import os
from utils.log import *
from utils.reply import send_message
from modules.src.db import Database
from modules.src.question import Question
from modules.src.answer import Answer
from modules.src.user import User
from modules.src.event import Event

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', config.VERIFY_TOKEN)
DATABASE_NAME = os.environ.get('DATABASE_NAME', config.DATABASE_NAME)
DATABASE_USER = os.environ.get('DATABASE_USER', config.DATABASE_USER)
DATABASE_PASS = os.environ.get('DATABASE_PASS', config.DATABASE_PASS)

app = Flask(__name__)
db = Database(DATABASE_NAME, DATABASE_USER, DATABASE_PASS)
event_handler = Event(db)
question_handler = Question(db, event_handler)
answer_handler = Answer(db, event_handler)
user_handler = User(db, event_handler)



@app.route('/')
def info():
    """

    :return:
    """
    return "Hi! I am Ubik. I will get the best people to answer your questions." \
        " Ask anything sensible. Also please don't include any personal details." \
        " This is an anonymous Q&A platform, built on confidence. " \
        "If you ask indecent questions, you will lose right to ask. " \
        "Similar rules apply for those who answer questions. But don't worry, I am there for you." \
        " Ohh! I forgot to tell you, I rose from dead."


@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    """

    :return:
    """
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
                        if messaging_event.get("message").get("quick_reply"):
                            feedback_payload = messaging_event["message"]["quick_reply"]["payload"]
                            handle_message(feedback_payload, sender_id, type= "feedback")
                        else:
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


def handle_message(payload, sender_id, type="non-feedback"):
    """

    :param message_text:
    :param sender_id:
    :return:
    """
    if type == "non-feedback":
        if payload == "about ubik":
            response_text = "Hi! I am Ubik.\n\nI am your personal Q&A (Question and Answer) bot. "\
                "I will get the best people to answer your questions." \
                " Ask anything sensible. But please [PLEASE] don't include any personal details, "\
                "as they will be delivered as it is to all users getting an A2A.\n" \
                "This is an anonymous Q&A platform, built on confidence." \
                " If you ask indecent questions or give inappropriate answers you will get substantial hit "\
                "to your karma score and may lose your access to my service. We get feedback on your questions and"\
                " answers and closely monitor them.\n"
        elif payload == "help":
            response_text = "1. To ask a question\n[Question] <Question Text> \n\n" \
                "Example:\n[Question] Who is Ubik ?\n" \
                "------------------------------\n\n" \
                "2. To give an answer\n[Answer][qid:<question id (qid)>] <Answer Text>\n\n" \
                "Example:\n[Answer][qid:1] Ubik is a Zombie who is getting younger by getting you answers " \
                "to your questions\n" \
                "------------------------------\n\n" \
                "3. For longer questions and answers (above 640 chars), use text pasting sites like\n"\
                " https://justpaste.it/ \n"\
                "and paste link at <Question Text> and <Answer Text> placeholder respectively."
        elif payload.startswith('[Question]'):
            question_handler.add_question(payload, sender_id)
            response_text = question_handler.fetch_response()
        elif payload.startswith('[Answer]'):
            answer_handler.add_answer(payload, sender_id)
            response_text = answer_handler.fetch_response()
        elif payload == 'ranking':
            response_text = user_handler.get_user_statistics(sender_id)
        else:
            response_text = "Hi, I am Ubik. You can ask me your question.\n"\
                    "Type 'about ubik' for knowing about me.\n"\
                    "Type 'help' for details on how to use me.\n"\
                    "Type 'ranking' for knowing your karma score."
    elif type == "feedback":
        response_text = event_handler.post_feedback(payload, user_handler)
    else:
        response_text = "invalid message type"

    send_message(sender_id, response_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
