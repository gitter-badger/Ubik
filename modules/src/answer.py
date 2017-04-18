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

import re


class Answer:
    def __init__(self, db, event_handler):
        """
        Handles answers posted to the Ubik platform.

        :param db: object for Postgres database.
        """
        self.db = db
        self.cur = db.get_cursor()
        self.event_handler = event_handler
        self.stored_answer = True

    def add_answer(self, text, responder_id):
        """
        Adds the answer for the corresponding question to the database.

        :param text: The text for the answer
        :param responder_id: The id of the person who answered the question
        :return: None
        """
        answer = text.split('[Answer]')[1].strip()
        m = re.search('\[(qid):([0-9]*)\]', answer)
        if m is not None:
            question_id = m.group(2)
            answer_text = answer.split('[qid:{0}]'.format(question_id)[1].strip()
            # stores present answer
            self.cur.execute(
                "INSERT INTO answer (answer, responder_id, question_id) VALUES (%s, %s, %s);",
                (answer_text, responder_id, question_id))
            self.cur.execute(
                "INSERT INTO users (user_id) SELECT (%s) WHERE NOT EXISTS (SELECT * FROM users WHERE user_id=%s);",
                (str(responder_id), str(responder_id)))
            self.event_handler.new_answer(question_id, answer, responder_id)
        else:
            self.stored_answer = False

    def fetch_response(self):
        """
        Sends a immediate feedback, explaining, if the answer was saved or not.

        :return: Feedback text.
        """
        if self.stored_answer:
            return "Thanks for your answer. Your answer has been saved. "\
                "I will get back to you when the destined asker, rates your response. "\
                "Keep your fingers crossed. Hopefully the asker will give you good ratings, "\
                "and your karma points will boost up."\
                "Meanwhile, you can ask another question, or post answer for requested question."
        else:
            self.stored_answer = True
            return "Sorry, you did not enter the Answer in the required format. "\
                "Eg - \"[Answer][qid:<placeholder for question_number>] <Placeholder for Answer>\". Try again"
