import psycopg2
import sys
from private import Private

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

class DatabaseOps(object):

    def __init__(self):
        pass
    '''
    Typically, the lhs_class is the database table names
    and the rhs_class is the data
    This class helps to assemle the data
    '''
    
    def import_classes(self, lhs_class, rhs_class, include_ids=True):       
        if lhs_class.__class__.__name__ == rhs_class.__class__.__name__:
            self.lhs = lhs_class
            self.rhs = rhs_class
            self.pair_values(include_ids)
            self.tablename = lhs_class.__class__.__name__.lower()
        else:
            self.__del__()
    
    def __del__(self):
        pass

    def pair_values(self, include_ids):
        self.value_pairs = {}
        for p in self.lhs.__dict__:
            self.value_pairs[self.lhs.__dict__[p]] = self.scrub_data(self.rhs.__dict__[p])
        
        if not include_ids:
            del self.value_pairs['id']
    
    def scrub_data(self, data):
        try:
            data.isdigit()                      # string method which fails if int
            data.replace("'","''")              # double up single-quotes to avoid sql error
        except:
            data =str(data)                     # cast int as string
        return data.encode('utf8', 'replace')
    
    def make_delimited_string(self, delim, is_key=True):
        if is_key:
            return delim.join('%s' % (k) for k,v in self.value_pairs.items())
        else:
            return delim.join('%s' % (v) for k,v in self.value_pairs.items())
    
    def make_insert_into_values(self):

        def scrub_int(value):
            if not value.isdigit():
                return "'"
            else:
                return ""
        
        comma_sep  = ', '.join("%s%s%s" % (scrub_int(v),v,scrub_int(v)) for k,v in self.value_pairs.items())
        return comma_sep        

    def build_insert(self):        
        sql = "INSERT INTO %s(%s) VALUES(%s)" % (self.tablename, self.make_delimited_string(', '), self.make_insert_into_values())
        return sql
    
    def build_csv(self, delim='|', is_header=False):
        string = "%s\n" % (self.make_delimited_string(delim, is_header))
        return string
    
    ### not used, but remain here if needed for debugging ###
    def print_record2(self):
        for k,v in self.value_pairs.items():
            print '%s = %s' % (k, v)
   
    def print_record(self):
        print self.value_pairs    