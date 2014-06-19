import os, urllib2, simplejson
from database import Database, DatabaseOps
from zipmarket import ZipMarket             #eventually push into models.py
from models import MarketDetails
import settings as s

class GivenRecords(object):
    def __init__(self, KeyArgs, sql):

        if sql != None:
            if KeyArgs.db != None:
                # pool the connection
                records = KeyArgs.db.fetch(sql)
            else:
                db = Database()
                records = db.fetch(sql)    
                db.close()
            self.records = records
            self.recordnum = 0
            self.recordcount = len(self.records)
        else:
            self.records = None
    
    ### these are all orphaned ###    
    def get_next_record(self):
        self.recordnum+=1
        return self.records[self.recordnum]
        
    def print_records(self):
        # records is a tuple
        for record in self.records:
            print record
    
    def print_fields(self):
        
        for record in self.records:
            # print record[0], record[1]
            for r in record:
                print r    
    


class ApiEngine(object):

    def __init__(self, url_var, url_pre, api_main_key, api_keys, api_err):
        self.url_pre = url_pre
        self.update_url(url_var)
        self.api_main_key = api_main_key
        self.api_keys = api_keys
        self.api_err = api_err
        self.count = 0
    
    def update_url(self, var):
        self.url_var = str(var)
        self.url = '%s%s' % (self.url_pre, self.url_var)
    
    def counter(self):
        self.count += 1
    
    def get_json(self):
        req = urllib2.Request(self.url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json = simplejson.load(f) 
        return json

    def parse_json(self, KeyArgs): #, json_columns):
        url = self.url
        json = self.get_json()
        
        # print self.api_main_key
        
        results = json[self.api_main_key]
        
        # print results
        
        def get_result(results):
            if type(results) == type({}):
                # if dict begin creating objects
                process_result(results)
            else:
                for result in results:
                    process_result(result)

        def process_result(result):

            # print self.api_err[0], self.api_err[1]
            """
            Explicit call to MarketDetails() here is weak
            As is passing the parameters individually
            ### NEEDS WORK ###
            """
            
            marketdetail = MarketDetails(KeyArgs.record[0],
                                         KeyArgs.record[1],
                                         result['Address'],
                                         result['GoogleLink'],
                                         result['Products'],
                                         result['Schedule']
                                         )
            
            sql_cols = MarketDetails(*KeyArgs.engine.sql_cols_list)
            
            sql = DatabaseOps()
            sql.import_classes(sql_cols, marketdetail)
            
            if KeyArgs.db != None:
                KeyArgs.db.query(sql.build_insert())
            else:
                line = sql.build_csv()
                print line
                KeyArgs.new_file.write(line)
        
        get_result(results)
        self.counter()

        
class Engine(object):
    '''
    this controls the instances of classes
    '''
    
    def init_cls(self, params):
        if self.cls =='zipmarket': 
            c = ZipMarket(*params),
        if self.cls =='marketdetails': 
            c = MarketDetails(*params)
        return c

    def __init__(self, columns, cls):
        self.cls = cls
        self.columns = columns
        self.unpack_columns()
    
    def unpack_columns(self):
        sql_cols = []
        sql_defs = []
        api_cols = []
        sql_declare = []
        
        for column in self.columns:
            sql_cols.append(column[0])          
            sql_declare.append(column[1])
            api_cols.append(column[2])
            # combine the column names with the declarations
            # // this could be improved
            sql_defs.append('%s %s' % (column[0],column[1])) 
        
        self.sql_cols_list = sql_cols    
        self.sql_cols = self.init_cls(sql_cols)
        self.sql_declare = self.init_cls(sql_declare)
        self.api_cols = self.init_cls(api_cols)
        
        self.sql_defs = sql_defs
        self.tablename = self.sql_cols.__class__.__name__.lower()
    
    # //TODO: move this do DatabaseOps() class, if possible.    
    def create_table(self):
        string = ', '.join('%s' % (k) for k in self.sql_defs)
        return 'CREATE TABLE %s(%s)' % (self.tablename, string)
        

class KeyArgs():
    
    def __init__(self, engine, write_to_db, record): # fix zip_start & zip_finish    
        self.engine = engine
        self.write_to_db = write_to_db
        self.record = record      
        
        if write_to_db:
            self.db = Database()
        else:
            self.db = None
            dbops = DatabaseOps()
            dbops.import_classes(engine.sql_cols, engine.sql_declare)
            self.tablename = dbops.tablename
            self.new_file = open('%s.csv' % (dbops.tablename), 'w')
            self.new_file.write(dbops.build_csv('|', True))
        
   

    
    
'''
if copying out to a csv:

in PSQL window

marketdetails:
\COPY marketdetails(schedule, googlelink, marketname, products, address, id) FROM C:\path\to\farmersmarkets\marketdetails.csv WITH CSV HEADER DELIMITER '|';

zipmarkets:
\COPY zipmarkets(zipcode, market_id, marketname) FROM C:\path\to\farmersmarkets\zipmarkets.csv WITH CSV HEADER DELIMITER '|';

'''
### ORPHANED ###
class ClassParser(object):

    def __init__(self, results, givens, json_columns):
        
        given.columns = []
        
        for column in json_columns:
            try:
                self.dict[column] = results[column]
            except:
                not_in_json.append(column)
        
        for item in not_in_json:
            self.dict[item] = givens[item]
        
        return self.dict    
    
    def return_dict(self):
        return self.dict