import optparse
import redis
import sys
import configparser

class url_lookup_service():

    def __init__(self,config_file=None):
        self.config_file = config_file
        self.db_info = {}
        self.get_config()

    def get_config(self):
        if self.config_file:
            config = configparser.ConfigParser()
            config.read(self.config_file)

            self.db_info['type'] = config['database']['type']
            if self.db_info['type'] == 'redis':
                self.db_info['host'] = config['redis']['host']
                self.db_info['port'] = config['redis']['port']
        else:
            self.db_info['type'] = 'in_memory'

    def setup(self):
        self.db_obj = url_malware_db(self.db_info)
        self.lookup_obj = url_db_lookup(self.db_obj)
        self.update_obj = url_db_update(self.db_obj)
        self.sync_obj = url_db_syncup(self.db_obj)
        print (" TODO setup web framework for HTTP requests")
        print (" TODO initial database syncup")

    def lookup_url(self,url):
        return self.lookup_obj.get_url_status(url)

    def update_url(self,url):
        self.update_obj.add_url(url)
        
class url_malware_db():
    def __init__(self,db_info):
        self.type = db_info['type'] 
        self.redis_set = 'malware'

        if self.type == 'in_memory':
            self.db = set()
        else:
            try:
                self.db = redis.Redis(host=db_info['host'],
                                           port=db_info['port'],
                                           db=0)
                self.db.ping()
            except (ConnectionRefusedError ,redis.exceptions.ConnectionError) as e:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
            except Exception as e:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])


class url_db_lookup():
    def __init__(self,db_obj):
        self.db_obj = db_obj

    def get_url_status(self,url):
        if self.db_obj.type == 'in_memory':
            return (url in self.db_obj.db)
        return (self.db_obj.db.sismember(self.db_obj.redis_set, url))

class url_db_update():

    def __init__(self,db_obj):
        self.db_obj = db_obj

    def add_url(self,url):
        if self.db_obj.type == 'in_memory':
            self.db_obj.db.add(url)
        else:
            self.db_obj.db.sadd(self.db_obj.redis_set, url)

class url_db_syncup(url_lookup_service):

    def __init__(self,db):
        self.db = db.db

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
        url_service.setup()
if __name__ == '__main__':
    main()
