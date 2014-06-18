# this needs to take the form of a LIST of TUPLES, columns in order
# each tuple should follow this format
# (<sql_column_name>, <sql_column_declaration>, <api_column_name>)
COLUMNS = [('id', 'INT PRIMARY KEY', '')
           ,('marketname', 'VARCHAR(255)', '')
           ,('address', 'VARCHAR(1000)', 'Address')
           ,('googlelink', 'VARCHAR(1000)', 'GoogleLink')
           ,('products', 'TEXT', 'Products')
           ,('schedule', 'VARCHAR(1000)', 'Schedule')
           ]

API_CLASS_NAME = 'marketdetails' # this should be called on by folder name

# this is the url string BEFORE the variables
API_URL = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id="

# this is the top level key when .json is returned
API_MAIN_KEY = 'marketdetails'

API_KEYS = ['Address', 'GoogleLink', 'Products','Schedule']

API_ERROR = ['Address', "Error, market not found."]

WRITE_TO_DB = False

# if the given list (URL_KEYs) comes from a sql table,
# then define the query in here.
def SQL_GIVEN_LIST():
    """
    SELECT market_id
            ,LTRIM(RTRIM(substr(marketname, strpos(marketname, ' ')+1)))
    FROM zipmarkets
    GROUP BY market_id
            ,LTRIM(RTRIM(substr(marketname, strpos(marketname, ' ')+1)))
    ORDER BY market_id
    """
    pass