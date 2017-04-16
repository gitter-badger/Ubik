class Question:
    def __init__(self, db):
        self.db = db
        self.cur = db.get_cursor()
        self.stored_question = True

    def add_question(self, text, sender_id):
        question = text.split('[Question]')[1].strip()
        try:
            self.cur.execute("INSERT INTO question (question, asker_id, has_answer) VALUES (%s, %s, %s)", (question, str(sender_id), False))
        except:
            self.stored_question = False

    def fetch_response(self):
        if self.stored_question:
            return "Your question has been saved. "\
            "I will get back to you with an expert's answer. "\
            "Keep your fingers crossed. "\
            "Meanwhile, you can ask another question, or post answer for requested question."
        else:
            self.stored_question = True
            return "Sorry, there has been some issue with our server. We are working hard to fix it up. Try again after sometime."
