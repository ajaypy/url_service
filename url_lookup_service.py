import optparse

class url_lookup_service():

    def __init__(self,config_file=None):
        self.config_file = config_file


    def setup(self):
        self.db_obj = url_malware_db()
        self.lookup_obj = url_db_lookup(self.db_obj)
        self.update_obj = url_db_update(self.db_obj)
        self.sync_obj = url_db_syncup(self.db_obj)
        print (" TODO setup the web framework to receive HTTP requests")
        print (" TODO setup redis and do initial database syncup")

    def lookup_url(self,url):
        return self.lookup_obj.get_url_status(url)

    def update_url(self,url):
        self.update_obj.add_malware_url(url)
        
class url_malware_db():
    def __init__(self):
        self.malware_db = set()

class url_db_lookup():
    def __init__(self,db):
        self.malware_db = db.malware_db

    def get_url_status(self,url):
        if url in self.malware_db:
            return True
        return False

class url_db_update():

    def __init__(self,db):
        self.malware_db = db.malware_db

    def add_malware_url(self,url):
        self.malware_db.add(url)

class url_db_syncup(url_lookup_service):

    def __init__(self,db):
        self.malware_db = db.malware_db

    def sync_malware_url(self,url):
        print ("TODO sync malware sync up database")

def main():
        usage = "usage: %prog [options]"
        parser = optparse.OptionParser(usage=usage)

        parser.add_option("-f", "--conf", help="url service config file in json format", default='None', dest='conf_file_name')
        (options, args) = parser.parse_args()

        if options.conf_file_name == 'None':
           print ("No service configuration supplied")
        url_service = url_lookup_service(options.conf_file_name)
        url_service.setup_service()
if __name__ == '__main__':
    main()
