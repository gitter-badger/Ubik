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
from utils.mathematics import percentile


class User:
    def __init__(self, db, event_handler):
        """
        Handles user statistics.

        :param db: object for Postgres database.
        :param event_handler: object for handling event triggers.
        """
        self.db = db
        self.cur = db.get_cursor()
        self.event_handler = event_handler
        self.stored_karma = True

    def update_karma(self, points, user_id):
        """
        Updates karma points of the users.

        :param points: Karma points to be added to the user.
        :param user_id: The unique facebook id of the user, whose karma is to be updated.
        :return: None
        """
        try:
            self.cur.execute("SELECT karma from users WHERE user_id=%s;", (user_id,))
            new_karma = int(self.cur.fetchone()[0]) + points
            self.cur.execute("UPDATE users SET karma=%s WHERE user_id=%s", (new_karma, user_id))
            return new_karma
        except:
            log("karma update failed")
            self.stored_karma = False

    def fetch_response(self):
        """
        fetches response to the feedback posted by the asker. Depends on the fact, that the karma was updated or not.

        :return: None
        """
        if self.stored_karma:
            return "Thanks for your feedback. Your feedback has been saved, "\
                   "and the person who answered will be notified."
        else:
            self.stored_karma = True
            return "Dang, our servers crashed. Lolzz. Finally something more than"\
                   " my brain can explode. Delicious tiny brain."

    def karma_updated(self):
        """
        Returns True, if the karma was updated. Else returns false.

        :return: True, if the karma was updated. Else returns false.
        """
        return self.stored_karma

    def get_user_statistics(self, user_id):
        """
        Obtain the user statistics like karma points, and percentile ranking of the users.

        :param user_id: The unique facebook id of the user whose statistics is requested.
        :return: Text with statistics embedded in it.
        """
        try:
            self.cur.execute("SELECT karma from users WHERE user_id=%s;", (user_id,))
            karma = int(self.cur.fetchone()[0])
            self.cur.execute("SELECT karma from users;")
            all_karmas = [x[0] for x in self.cur.fetchall()]
            percentile_standing = percentile(karma, all_karmas)
            if percentile_standing == -1:
                return "You need to ask at least one question, to be rated."
            else:
                return "Your karma score is:{0}\nYour karma score is above {1} percent of other users".format(karma, percentile_standing)
        except:
            return "Sorry, we don't have ranking for you. Ask a question first."

    def update_subscription(self, user_id, flag):
        """
        Update the subscription status of the users.

        :param user_id: Facebook id of the user whose subscription status is to be updated.
        :param flag: True, means subscription should be made active, False, means subscription should be made inactive.
        :return: Feedback for the subscription update.
        """
        try:
            self.cur.execute("UPDATE users SET subscription=%s WHERE user_id=%s;", (flag, user_id))
            if flag:
                return "Welcome back! Your subscription has been restarted. Best of luck answering questions."
            else:
                return "Your subscription has been paused. \n"\
                       "For each day your subscription is inactive, you lose 10 karma points"
        except:
            log("subscription update failed")
            return "We were unable to update your subscription. We are working to fix this up. Sorry, says the Zombie."




