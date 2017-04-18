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

import psycopg2
from utils.log import *
from utils.database_parser import parse_database


class Database:
    def __init__(self, db_url):
        """
        Database in which question, answers, and user information is posted.

        :param db_url: The url of the server hosting the database.
        """
        self.conn = None
        db_user, db_pass, db_host, db_port, db_name = parse_database(db_url)
        try:
            self.conn=psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'".
                format(db_name, db_user, db_host, db_port, db_pass))
            self.conn.autocommit = True
        except:
            log("I am unable to connect to the database. Credentials are\n"\
                "dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'".
                format(db_name, db_user, db_host, db_port, db_pass))

    def connected(self):
        """
        Sends boolean status of the database

        :return: True, if the connection is established, else False
        """
        return self.conn is not None

    def get_cursor(self):
        """
        Sends database cursor, to update the database.

        :return: database cursor.
        """
        return self.conn.cursor()
