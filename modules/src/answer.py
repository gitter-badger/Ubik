import re

class Answer:
    def __init__(self, db):
        self.db = db
        self.cur = db.get_cursor()
        self.stored_answer = True

    def add_answer(self, text, sender_id):
        answer = text.split('[Answer]')[1].strip()
        m = re.search('\[(qid):([0-9]*)\]', answer)
        if m != None:
            question_id = m.group(2)
            # stores present answer
            self.cur.execute("INSERT INTO answer (answer, responder_id, question_id) VALUES (%s, %s, %s)", (answer, sender_id, question_id))
        else:
            self.stored_answer = False


    def fetch_response(self):
        if self.stored_answer:
            return "Thanks for your answer. Your answer has been saved. "\
            "I will get back to you when the destined asker, rates your response. "\
            "Keep your fingers crossed. Hopefully the asker will give you good ratings, and your karma points will boost up."\
            "Meanwhile, you can ask another question, or post answer for requested question."
        else:
            self.stored_answer = True
            return "Sorry, you did not enter the Answer in the required format. Eg - \"[Answer][qid:<placeholder for question_number>] <Placeholder for Answer>\". Try again"
