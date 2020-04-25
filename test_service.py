import unittest
from url_lookup_service import *


class Test_Service_init_in_memory_db(unittest.TestCase):

    def setUp(self):
        self.service = url_lookup_service()
        self.service.setup()

    def test_init(self):
        assert len(self.service.db_obj.db) == 0

class Test_url_update(unittest.TestCase):
    def setUp(self):
        self.service = url_lookup_service()
        self.service.setup()

        self.updated_urls = ['test_url1','test_url2']
        self.missing_urls = ['test_url3','test_url4']

        for url in self.updated_urls:
            self.service.update_url(url)

    def test_update_present(self):
        for url in self.updated_urls:
            assert (url in self.service.db_obj.db), "missing url %s" % url

    def test_update_absent(self):
        for url in self.missing_urls:
            assert(url not in self.service.db_obj.db), "extra url %s" % url


class Test_url_lookup(unittest.TestCase):
    def setUp(self):
        self.service = url_lookup_service()
        self.service.setup()

        self.updated_urls = ['test_url1','test_url2']
        self.missing_urls = ['test_url3','test_url4']

        for url in self.updated_urls:
            self.service.db_obj.db.add(url)

    def test_lookup_present(self):
        for url in self.updated_urls:
            assert (self.service.lookup_url(url)), "missing url %s" % url

    def test_lookup_absent(self):
        for url in self.missing_urls:
            assert (not self.service.lookup_url(url)), "extra url %s" % url

class Test_url_update_scale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = url_lookup_service()
        cls.service.setup()

        cls.updated_urls = []
        for i in range(5000):
            cls.updated_urls.append('malware_' + str(i))
        cls.missing_urls = ['missing_url1','missing_url2']

        for url in cls.updated_urls:
            cls.service.update_url(url)

    def test_update_present(self):
        for url in self.updated_urls:
            assert (url in self.service.db_obj.db), "missing url %s" % url

    def test_update_absent(self):
        for url in self.missing_urls:
            assert(url not in self.service.db_obj.db), "extra url %s" % url


class Test_Service_init_redis_db(unittest.TestCase):

    def setUp(self):
        self.service = url_lookup_service()
        self.service.db_info['type'] = 'redis'
        self.service.db_info['host'] = 'localhost'
        self.service.db_info['port'] = 6379
        self.service.setup()

    def test_init(self):
        db_obj = self.service.db_obj
        assert (db_obj.db.scard(db_obj.redis_set) == 0), "redis database is not empty"

class Test_url_update_scale_redis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = url_lookup_service()
        cls.service.db_info['type'] = 'redis'
        cls.service.db_info['host'] = 'localhost'
        cls.service.db_info['port'] = 6379
        cls.service.setup()

        cls.updated_urls = []
        for i in range(5000):
            cls.updated_urls.append('malware_' + str(i))
        cls.missing_urls = ['missing_url1','missing_url2']

        for url in cls.updated_urls:
            cls.service.update_url(url)

    def test_update_present(self):
        db_obj = self.service.db_obj
        for url in self.updated_urls:
            assert (db_obj.db.sismember(db_obj.redis_set,url)), "missing url %s" % url

    def test_update_absent(self):
        db_obj = self.service.db_obj
        for url in self.missing_urls:
            assert (not db_obj.db.sismember(db_obj.redis_set,url)), "extra url %s" % url

if __name__ == '__main__':
    unittest.main()
