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
from utils.log import log


class Question:
    def __init__(self, db, event_handler):
        """
        Handles questions posted to the Ubik platform.

        :param db: object for Postgres database.
        """
        self.db = db
        self.cur = db.get_cursor()
        self.event_handler = event_handler
        self.stored_question = True

    def add_question(self, text, asker_id):
        """
        Adds the question to the database

        :param text: The test of the question
        :param asker_id: The person who asked the question
        :return: None
        """
        question = text.split('[Question]')[1].strip()
        try:
            self.cur.execute(
                "INSERT INTO question (question, asker_id, has_answer) VALUES (%s, %s, %s) RETURNING question_id;",
                (question, str(asker_id), False))
            question_id = self.cur.fetchone()[0]
            self.cur.execute(
                "INSERT INTO users (user_id) SELECT (%s) WHERE NOT EXISTS (SELECT * FROM users WHERE user_id=%s);",
                (str(asker_id),str(asker_id)))
            self.event_handler.new_question(question_id)
        except:
            self.stored_question = False

    def fetch_response(self):
        """
        Sends a immediate feedback, explaining, if the question was saved or not.

        :return: Feedback message
        """
        if self.stored_question:
            return "Your question has been saved. "\
                "I will get back to you with an expert's answer. "\
                "Keep your fingers crossed. "\
                "Meanwhile, you can ask another question, or post answer for requested question."
        else:
            self.stored_question = True
            return "Sorry, there has been some issue with our server. We are working hard to fix it up. "\
                "Try again after sometime."

    def mark_question_as_resolved(self, question_id):
        try:
            self.cur.execute(
                "UPDATE question SET has_answer=TRUE WHERE question_id=%s",
                (question_id,)
            )
        except:
            log("question reolution db update failed")

