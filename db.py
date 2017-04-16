import psycopg2
from utils.log import *

class Database:
    def __init__(self, dbname, dbuser, dbpass):
        self.conn = None
        try:
            self.conn=psycopg2.connect(
                "dbname='{0}' user='{1}' host='localhost' password='{2}'".
                format(dbname, dbuser, dbpass))
            self.conn.autocommit = True
        except:
            log("I am unable to connect to the database.")

    def connected(self):
        return self.conn != None

    def get_cursor(self):
        return self.conn.cursor()
