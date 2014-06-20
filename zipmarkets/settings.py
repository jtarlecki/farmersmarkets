# this needs to take the form of a LIST of TUPLES, columns in order
# each tuple should follow this format
# (<sql_column_name>, <sql_column_declaration>, <api_column_name>)
COLUMNS = [('id', 'SERIAL PRIMARY KEY', '')
           ,('zipcode', 'VARCHAR(5)', '')
           ,('market_id', 'INT', 'id')
           ,('marketname', 'VARCHAR(255)', 'marketname')
           ]

API_CLASS_NAME = 'zipmarkets' # this should be called on by folder name

# this is the url string BEFORE the variables
API_URL = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/zipSearch?zip="

# this is the top level key when .json is returned
API_MAIN_KEY = 'results'

API_KEYS = ['id', 'marketname']

API_ERROR = ['id', 'Error']

WRITE_TO_DB = False

# Set to "True" if Id numbers are desired for the output
# If the database will create and Id automatically (say, SERIAL datatype); set to "False"
INCLUDE_IDS = False

# if the given list (URL_KEYs) comes from a sql table,
# then define the query in here.

def SQL_GIVEN_LIST(self):
    pass

'''
!!!!!!
Still need to find a way to manage the query (zip=1 to 100000)
and iterate
and how to dynamically recognize what settings file we are using for which run
!!!!!!!
'''
