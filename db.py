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


class Database:
    def __init__(self, dbname, dbuser, dbpass):
        """

        :param dbname:
        :param dbuser:
        :param dbpass:
        """
        self.conn = None
        try:
            self.conn=psycopg2.connect(
                "dbname='{0}' user='{1}' host='localhost' password='{2}'".
                format(dbname, dbuser, dbpass))
            self.conn.autocommit = True
        except:
            log("I am unable to connect to the database.")

    def connected(self):
        """

        :return:
        """
        return self.conn is not None

    def get_cursor(self):
        """

        :return:
        """
        return self.conn.cursor()
