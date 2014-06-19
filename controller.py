import os, urllib2, simplejson
from database import Database, DatabaseOps
#from zipmarkets.zipmarket import ZipMarket             #eventually push into models.py
from models import MarketDetails, ZipMarket
#import marketdetails.settings as settings

'''
### GENERAL TODO OTES ####

All instantiations of DatabaseOps() are followed by DatabaseOps().import_classes() method; perhaps consolodate call
Think about changing the name of DatabaseOps().  It assemlbles stings to be written to a CSV.
'''

class Settings():
    
    def __init__(self, module):
        
        # first, dynamically import correct settings module
        settings = __import__("%s.settings" % (module), fromlist=["%s" % (module)])
        print "successfully imported %s" % ("%s.settings" % (module))
        
        self.COLUMNS = settings.COLUMNS
        self.API_CLASS_NAME = settings.API_CLASS_NAME
        self.API_URL = settings.API_URL
        self.API_MAIN_KEY = settings.API_MAIN_KEY
        self.API_KEYS = settings.API_KEYS
        self.API_ERROR = settings.API_ERROR
        self.WRITE_TO_DB = settings.WRITE_TO_DB
        self.SQL_GIVEN_LIST = settings.SQL_GIVEN_LIST.__doc__   

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
    
    ### these are all orphaned, but here if you need them to debug ###    
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

class KeyArgs():
    
    def __init__(self, settings): # fix zip_start & zip_finish    
        # instantiates Engine() class
        # and DatabaseOps() class, if writing to CSV (name convention seems counter intuitive)
        self.settings = settings
        self.engine = Engine(settings)
        self.write_to_db = settings.WRITE_TO_DB
        
        if settings.WRITE_TO_DB:
            self.db = Database()
        else:
            self.db = None
            self.new_file = open('%s.csv' % (self.engine.tablename), 'w')
            
            dbops = DatabaseOps()
            dbops.import_classes(self.engine.sql_cols, self.engine.sql_declare)
            self.new_file.write(dbops.build_csv('|', True))

class Engine(object):
    '''
    this controls the instances of classes
    perhaps the init_cls could be better control by packaging up
    modules into folders, and have the folder be recognized
    '''
    def init_cls(self, params):
        if self.cls =='zipmarket': 
            c = ZipMarket(*params),
        if self.cls =='marketdetails': 
            c = MarketDetails(*params)
        return c

    def __init__(self, settings):
        self.cls = settings.API_CLASS_NAME
        self.columns = settings.COLUMNS
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

class ApiEngine(object):
    '''
    // TODO: need to divorce ApiEngine() properties from Settings() properties 
    doing some double duty here
    '''
    
    def __init__(self, settings):
        self.settings = settings
        self.url_var = ''
        #self.url_pre = url_pre
        ##self.update_url(url_var)
        #self.api_main_key = api_main_key
        #self.api_keys = api_keys
        #self.api_err = api_err
        self.count = 0
    
    def update_url(self, var):
        #self.url_var = str(var)
        #self.url = '%s%s' % (self.url_pre, self.url_var)
        self.url_var = str(var)
        self.url = '%s%s' % (self.settings.API_URL, self.url_var)
        
    def counter(self):
        self.count += 1
    
    def get_json(self):
        req = urllib2.Request(self.url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json = simplejson.load(f) 
        return json

    def parse_json(self, KeyArgs): 
        url = self.url
        json = self.get_json()   
        results = json[self.settings.API_MAIN_KEY]

        def get_result(results):
            if type(results) == type({}):
                # if dict begin creating objects
                process_result(results)
            else:
                for result in results:
                    process_result(result)

        def get_result_list(GivenRec, result):
            args = list(GivenRec) #force the tuple to be a list           
            
            for k in self.settings.API_KEYS:
                args.append(result[k])
            
            return args
        
        def process_result(result):
            
            #s = Settings() #mostly a static variable class
            args = get_result_list(KeyArgs.record, result)

            data = KeyArgs.engine.init_cls(args)
            sql_cols = KeyArgs.engine.init_cls(KeyArgs.engine.sql_cols_list)
            
            sql = DatabaseOps()
            sql.import_classes(sql_cols, data)
            
            if KeyArgs.db != None:
                KeyArgs.db.query(sql.build_insert())
            else:
                line = sql.build_csv()
                print line
                KeyArgs.new_file.write(line)
        
        get_result(results)
        self.counter()
    
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