class MarketDetails(object):

    def __init__(self, identity, marketname, address, googlelink, products, schedule):
        self.identity = identity
        self.marketname = marketname
        self.address = address
        self.googlelink = googlelink
        self.products = products
        self.schedule = schedule

class DatabaseOps(object):
    
    
    
    def __init__(self):
        pass
    
    def import_classes(self, lhs_class, rhs_class, include_ids=True):       
        if lhs_class.__class__.__name__ == rhs_class.__class__.__name__:
            self.lhs = lhs_class
            self.rhs = rhs_class
            self.pair_values(include_ids)
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
            data.isdigit()                  # string method which fails if int
            return data.replace("'","''")   # double up single-quotes to avoid sql error
        except:
            return str(data)                # cast int as string
    
    def print_record2(self):
        for k,v in self.value_pairs.items():
            print '%s = %s' % (k, v)
   
    def print_record(self):
        print self.value_pairs
    
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
        # // TO DO:
        # only thing left to clean up, bring in table name into class.        
        sql = "INSERT INTO %s(%s) VALUES(%s)" % ('marketdetails', self.make_delimited_string(', '), self.make_insert_into_values())
        return sql
    
    def build_csv(self, delim='|', is_header=False):
        string = "%s\n" % (self.make_delimited_string(delim, is_header))
        output_string = string.encode('utf8', 'replace')
        return output_string

sql_column_names = MarketDetails('id', 'marketname', 'address', 'googlelink', 'products', 'schedule')
sql_column_declarations = MarketDetails('INT PRIMARY KEY', 'VARCHAR(255)', 'VARCHAR(1000)', 'VARCHAR(1000)', 'TEXT', 'VARCHAR(1000)')
md = MarketDetails(1,"jay's, market",'1034 wolf st', "www.google.com", 'beer', 'daily')


dbops = DatabaseOps()
dbops.import_classes(sql_column_names, md)

print dbops.value_pairs

dbops.print_record2()
dbops.print_record()

dbops.make_delimited_string(', ')
print dbops.make_insert_into_values()
print dbops.build_insert()
print dbops.build_csv('|',True)
print dbops.build_csv('|',False)


print md.__dict__

for k,v in md.__dict__.items():
    print k,v

print md.__class__
print md.__class__.__name__

for k in md.__dict__:
    print k
    





"""
KeyArgs.db.create_table("CREATE TABLE %s(id SERIAL PRIMARY KEY, zipcode VARCHAR(5), market_id INT, marketname VARCHAR(255))" % (KeyArgs.tablename), KeyArgs.tablename)        
"""
"""
columns = [
    {'id': 'SERIAL PRIMARY KEY'},
    {'zipcode': 'VARCHAR(5)'},
    {'market_id': 'INT'},
    {'marketname':'VARCHAR(5)'}
]

string = []

for column in columns:    
    name = column.keys()[0]
    string.append("%s %s" % (name, column[name])) 

print ', '.join(string)
"""

"""
let = ['a','b','c','d']
num = [1,2,3,4]

if len(let) == len(num):
    for i in range(len(let)):
        print '%s = %s' % (let[i], num[i])
else:
    print 'two arrays do not have same length'
"""