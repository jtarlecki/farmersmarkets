import psycopg2
import sys
from private import *

class Database(Private):
    
    def __init__(self):
        Private.__init__(self)
        self.conn_string = "host=%s dbname=%s user=%s password=%s" % (self.host, self.dbname, self.user, self.password)
        print "Connecting to database\n -> %s %s" % (self.host, self.dbname)
        self.conn = psycopg2.connect(self.conn_string)
        self.cur = self.conn.cursor()
        print "Connected!\nWelcome %s" % (self.user)

    def query(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        
    def create_table(self, sql, tablename):
        self.drop_table(tablename)
        self.query(sql)
        
    def drop_table(self, tablename):
        self.query('DROP TABLE IF EXISTS %s;' % (tablename))
    
    def close(self):
        self.conn.close()
        
    def fetch(self, sql):
        self.query(sql)
        return self.cur.fetchall() # returns a tuple of tuples
