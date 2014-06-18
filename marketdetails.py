import os
import urllib2
import simplejson
from database import Database, DatabaseOps
from zipmarket import ZipMarket

def sql_marketids():
    """
    SELECT market_id
            ,LTRIM(RTRIM(substr(marketname, strpos(marketname, ' ')+1)))
    FROM zipmarkets
    GROUP BY market_id
            ,LTRIM(RTRIM(substr(marketname, strpos(marketname, ' ')+1)))
    ORDER BY market_id
    """
    pass

def print_records(records):
    # records is a tuple
    for record in records:
        print record

def print_fields(records):
    
    for record in records:
        # print record[0], record[1]
        for r in record:
            print r    

def test_db():
    
    db = Database()
    records = db.fetch(sql_marketids.__doc__)    
    db.close()
    return records


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

class MarketDetails(object):

    def __init__(self, identity, marketname, address, googlelink, products, schedule):
        self.identity = identity
        self.marketname = marketname
        self.address = address
        self.googlelink = googlelink
        self.products = products
        self.schedule = schedule
        
#class MarketDetailsDefinitions(MarketDetails):
    
    #def __init__(self):
        #sql

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
            I think the only way to do this is to pass a dict to MarketDetails
            and/or do the same for ZipMarket
            ...there's no way out of getting specific for the database models (classes).
            unless the classes can recognize and instance themselves.             
            """
            md = MarketDetails(KeyArgs.record[0],
                               KeyArgs.record[1],
                               result['Address'],
                               result['GoogleLink'],
                               result['Products'],
                               result['Schedule'])
            
            sql_cols = MarketDetails('id', 'marketname', 'address', 'googlelink', 'products', 'schedule')
            
            sql = DatabaseOps()
            sql.import_classes(sql_cols, md)
            
            #cls = Engine(SQL_columns)
            #z = ZipMarket(i, zipcode, result['id'],result['marketname'], KeyArgs.tablename)
            #z.print_record()
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
    this controls the instance of classes
    '''
    '''
    classes = {
        'ZipMarket': ZipMarket(),
        'MarketDetails': MarketDetails()
    }
    '''
    def __init__(self, cls, given_list, record_list):
        instantiate_class(cls)
        
    def instantiate_class(cls):
        cls_name = cls.__class__.__name__
        return self.classes.get(cls_name)

class KeyArgs():
    
    def __init__(self, tablename, write_to_db, record): # fix zip_start & zip_finish    
        self.tablename = tablename
        #self.columns = columns
        self.write_to_db = write_to_db
        self.record = record
        
        sql_column_names = MarketDetails('id'
                                         ,'marketname'
                                         ,'address'
                                         ,'googlelink'
                                         ,'products'
                                         ,'schedule'
                                         )
        
        sql_column_declarations = MarketDetails('INT PRIMARY KEY'
                                                ,'VARCHAR(255)'
                                                ,'VARCHAR(1000)'
                                                ,'VARCHAR(1000)'
                                                ,'TEXT'
                                                ,'VARCHAR(1000)'
                                                )
        
        api_column_names = MarketDetails(''
                                         ,''
                                         ,'Address'
                                         ,'GoogleLink'
                                         ,'Products'
                                         ,'Schedule'
                                         )        
        
        if write_to_db:
            self.db = Database()
        else:
            self.db = None
            self.new_file = open('%s.csv' % (self.tablename), 'w')
            dbops = DatabaseOps()
            dbops.import_classes(sql_column_names, sql_column_declarations)
            self.new_file.write(dbops.build_csv('|', True))

    
def test():
    
    a = ApiEngine(19104,"http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id=",
                  'marketdetails',
                  ['Address', 'GoogleLink', 'Products','Schedule'],
                  ['Address', "Error, market not found."]
                  )    

    recs = test_db()
    
    write_to_db = False
    
    columns = [
        {'id': 'INT PRIMARY KEY'},
        {'marketname':'VARCHAR(255)'},
        {'address': 'VARCHAR(1000)'},
        {'googlelink': 'VARCHAR(1000)'},
        {'products': 'TEXT'},
        {'schedule': 'VARCHAR(1000)'}
    ]            
    
    k = KeyArgs('marketdetails', write_to_db, '')

    if k.db != None:
        # column_declare = ', '.join('%s %s' % (k,v) for k,v in columns.items())
        string = []
        for column in columns:    
            name = column.keys()[0]
            string.append("%s %s" % (name, column[name])) 
        
        column_declare = ', '.join(string)          
        k.db.create_table("CREATE TABLE %s(%s)" % (k.tablename, column_declare), k.tablename)
    
    try:
        print len(recs)
        i = 0
        for rec in recs:
            i+=1
            k.record = rec
            a.update_url(rec[0]) # url_var
            a.parse_json(k)
    
    except:
        if write_to_db:
            k.db.rollback()
        print 'error at: i = ', i,'; count = ', a.count, rec[0], rec[1] 
    
    finally:
        if write_to_db:
            k.db.rollback()
            k.db.close()
        else:
            k.new_file.close()
    
def test2():
    
    col_names = [('id', 'INT PRIMARY KEY', '')
                 ,('marketname', 'VARCHAR(255)', '')
                 ,('address', 'VARCHAR(1000)', 'Address')
                 ,('googlelink', 'VARCHAR(1000)', 'GoogleLink')
                 ,('products', 'TEXT', 'Products')
                 ,('schedule', 'VARCHAR(1000)', 'Schedule')
                 ]
    
    sql_column_names = MarketDetails('id'
                                     ,'marketname'
                                     ,'address'
                                     ,'googlelink'
                                     ,'products'
                                     ,'schedule'
                                     )
    
    sql_column_declarations = MarketDetails('INT PRIMARY KEY'
                                            ,'VARCHAR(255)'
                                            ,'VARCHAR(1000)'
                                            ,'VARCHAR(1000)'
                                            ,'TEXT'
                                            ,'VARCHAR(1000)'
                                            )
    
    api_column_names = MarketDetails(''
                                     ,''
                                     ,'Address'
                                     ,'GoogleLink'
                                     ,'Products'
                                     ,'Schedule'
                                     ) 

    

    
if __name__ == '__main__':
    test()
    
    
'''
if copying out to a csv:

in PSQL window

marketdetails:
\COPY marketdetails(schedule, googlelink, marketname, products, address, id) FROM C:\path\to\farmersmarkets\marketdetails.csv WITH CSV HEADER DELIMITER '|';

zipmarkets:
\COPY zipmarkets(zipcode, market_id, marketname) FROM C:\path\to\farmersmarkets\zipmarkets.csv WITH CSV HEADER DELIMITER '|';

'''