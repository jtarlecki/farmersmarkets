import os
import urllib2
import simplejson
from database import *

class ZipMarket(object):
    
    def __init__(self, identity, zipcode, market_id, marketname, tablename):
        self.identity = identity
        self.zipcode = zipcode
        self.market_id = market_id
        self.marketname = marketname.replace("'","''") # double up single-quotes to avoid sql error
        self.tablename = tablename
    
    def print_record(self):
        print 'id = %d' %(self.identity), 'zipcode = %d' % (self.zipcode), 'market_id = %s' % (self.market_id), 'marketname = %s' % (self.marketname)
        
    def build_insert(self):
        sql = "INSERT INTO %s(zipcode, market_id, marketname) VALUES('%d', %s, '%s')" % (self.tablename, self.zipcode, self.market_id, self.marketname)
        return sql
    
    def build_csv(self):
        string = "%d|%s|%s\n" % (self.zipcode, self.market_id, self.marketname)
        output_string = string.encode('utf8', 'replace')
        return output_string

def get_json(self):
    req = urllib2.Request(self.url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    return json    

def print_json(i, zipcode, KeyArgs):
    url = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/zipSearch?zip=%d"  % (zipcode)
    json = get_json(url)

    results = json['results']

    for result in results:
        if result['id'] != 'Error':
            i+=1
            z = ZipMarket(i, zipcode, result['id'],result['marketname'], KeyArgs.tablename)
            #z.print_record()
            if KeyArgs.db != None:
                KeyArgs.db.query(z.build_insert())
            else:
                KeyArgs.new_file.write(z.build_csv())
    return i


class KeyArgs():
    
    def __init__(self, tablename, columns, write_to_db, zip_start, zip_finish): # zip_start and zip_finish not generic enough
        self.tablename = tablename
        self.columns = columns
        self.write_to_db = write_to_db
        self.zip_start = zip_start
        self.zip_finish = zip_finish
        if write_to_db:
            self.db = Database()
        else:
            self.db = None
            self.new_file = open('%s.csv' % (self.tablename), 'w')
            
def run(KeyArgs):
    i=0
    if KeyArgs.db != None:
        """
        Then, write each record to a databse table
        This is slow if database is remote!
        """
        
        string = []
        
        for column in KeyArgs.columns:    
            name = column.keys()[0]
            string.append("%s %s" % (name, column[name])) 
        
        column_declare = ', '.join(string)
        
        KeyArgs.db.create_table("CREATE TABLE %s(%s)" % (KeyArgs.tablename, column_declare), KeyArgs.tablename)        
    else:
        """
        else: create a new csv file
        and write each record to the file (faster)
        Seprately, you can bulk add the entire csv to a databse.
        """
        
        KeyArgs.new_file.write("zipcode|market_id|marketname\n")      # csv header        

    for zip_int in range(KeyArgs.zip_start, KeyArgs.zip_finish):
        print '------------------- %d %d -------------------' % (i, zip_int)
        i = print_json(i, zip_int, KeyArgs)
    
    if KeyArgs.db == None:    
        abs_path = os.path.abspath(KeyArgs.new_file.name)
        print "PSQL script to bulk copy this csv into database:\n"
        print "\COPY %s FROM %s WITH CSV HEADER DELIMTER '|';" % (KeyArgs.tablename, abs_path)
        KeyArgs.new_file.close()
        
    print 'COMPLETE: %d RECORDS GRABBED' % (i)



def run_test(columns):
    """
    2nd arg of "KeyArgs" = write_to_db:
    True = write to a databse
    False = write to csv... csv is actually pipe (|) delimited
    """
    # key = KeyArgs('zipmarkets2', columns, True, 19100, 19120)  # write to database
    key = KeyArgs('zipmarkets2', columns, False, 19100, 19120)  # write to csv
    run(key)

def run_live(columns):
    key = KeyArgs('zipmarkets', columns, False, 10000, 100000)
    run(key)

if __name__ == "__main__":
    columns = [
        {'id': 'SERIAL PRIMARY KEY'},
        {'zipcode': 'VARCHAR(5)'},
        {'market_id': 'INT'},
        {'marketname':'VARCHAR(255)'}
    ]        
    run_test(columns)
    # run_live()