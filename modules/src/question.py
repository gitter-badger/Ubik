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


class Question:
    def __init__(self, db):
        """

        :param db:
        """
        self.db = db
        self.cur = db.get_cursor()
        self.stored_question = True

    def add_question(self, text, sender_id):
        """

        :param text:
        :param sender_id:
        :return:
        """
        question = text.split('[Question]')[1].strip()
        try:
            self.cur.execute("INSERT INTO question (question, asker_id, has_answer) VALUES (%s, %s, %s)",
                             (question, str(sender_id), False))
        except:
            self.stored_question = False

    def fetch_response(self):
        """

        :return:
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
