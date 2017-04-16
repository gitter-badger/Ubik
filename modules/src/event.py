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

from utils.reply import send_message, get_feedback
import random
from utils.log import log

class Event:
    def __init__(self, db):
        """

        :param db:
        :param question_handler:
        :param answer_handler:
        :param user_handler:
        """
        self.db = db
        self.cur = db.get_cursor()

    def new_question(self, question_id):
        """
        Triggered when a new question is asked.
        Response: If number of users = 1, do nothing
                                     = 2, send question to the non-asker
                                     = 2+, send question to (n - 1)/2 non-askers

        :param question_id:

        :return:
        """
        self.cur.execute("SELECT asker_id, question FROM question WHERE question_id=%s;", (question_id,))
        asker_id, question = self.cur.fetchone()
        self.cur.execute("SELECT DISTINCT user_id FROM users WHERE user_id != %s;", (asker_id,))
        non_askers = [x[0] for x in self.cur.fetchall()]
        if not non_askers:
            return

        request_message = "Can you answer this question? coz I can't as I don't have brains "
        question_message = "[Question][qid:{0}] {1}".format(question_id, question)
        if len(non_askers) == 1:
            send_message(int(non_askers[0]), request_message)
            send_message(int(non_askers[0]), question_message)
        else:
            chosen_non_askers = random.sample(non_askers, (len(non_askers) - 1) / 2)
            for recipient in chosen_non_askers:
                send_message(int(recipient), request_message)
                send_message(int(recipient), question_message)

    def new_answer(self, question_id, answer, sender_id):
        """
        Triggered when a new answer is given.
        Response: If has_answer = True, do nothing (as user is satisfied)
                                else, send asker the answer, and ask if he is satisfied.

        :param question_id:
        :param answer:
        :param sender_id:
        :return:
        """
        """
        Triggered when a new answer is given.

        :return:
        """
        self.cur.execute("SELECT asker_id, question, has_answer FROM question WHERE question_id=%s;", (question_id,))
        asker_id, question, has_answer = self.cur.fetchone()

        if has_answer:
            return
        if asker_id == sender_id:
            return

        respond_message = "Here is the answer to your question\n{0}".format(question)
        answer_message = "[Answer]\n {0}".format(answer)
        send_message(int(asker_id), respond_message)
        send_message(int(asker_id), answer_message)
        get_feedback(int(asker_id), int(sender_id), question)

    def ask_answer(self):
        """
        Triggered periodically, asking for an answer.

        :return:
        """
        pass

    def post_feedback(self, feedback_payload, user_handler):
        points, rating, answerer_id, question = [x.strip() for x in feedback_payload.split(',')]
        karma = user_handler.update_karma(int(points), answerer_id)
        # send karma info to the answerer
        if user_handler.karma_updated():
            respond_message = "Hey dude, someone rated you ({0}), for Question: {1}. Your current karma point is: {2}".format(rating, question, karma)
            send_message(int(answerer_id), respond_message)

        return user_handler.fetch_response()

    '''
    def remind_to_answer(self):
        """
        Triggered periodically, to remind a user for an answer.

        :return:
        """
    '''
