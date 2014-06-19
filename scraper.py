from controller import *

class Scraper():
    
    def __init__(self, module):
        s = Settings(module)
        a = ApiEngine(s)    
        k = KeyArgs(s)        

        self.settings = s
        self.api = a
        self.keyargs = k

    def run(self):
        given = GivenRecords(self.keyargs, self.settings.SQL_GIVEN_LIST)
        recs = given.records
        
        if self.keyargs.db != None:         
            self.keyargs.db.create_table(self.keyargs.engine.create_table()) # looks like it should be moved out of Engine()
    
        try:
            print len(recs)
            i = 0
            for rec in recs:
                i+=1
                self.keyargs.record = rec
                self.api.update_url(rec[0]) # url_var
                self.api.parse_json(self.keyargs)
        
        except:
            if self.settings.WRITE_TO_DB:
                self.keyargs.db.rollback()
            print 'error at: i = ', i,'; count = ', self.api.count, rec[0], rec[1] 
        
        finally:
            if self.settings.WRITE_TO_DB:
                self.keyargs.db.rollback()  ### NEEDS WORK ###
                self.keyargs.db.close()
            else:
                self.keyargs.new_file.close()


if __name__ == '__main__':
    scraper = Scraper('zipmarkets')
    scraper.run()