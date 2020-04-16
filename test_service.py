import unittest

from x import *


class Test_Service_init_in_memory_db(unittest.TestCase):

    def setUp(self):
        self.service = url_lookup_service()
        self.service.setup()

    def test_init(self):
        assert len(self.service.db_obj.malware_db) == 0

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
            assert (url in self.service.db_obj.malware_db), "missing url %s" % url

    def test_update_absent(self):
        for url in self.missing_urls:
            assert(url not in self.service.db_obj.malware_db), "extra url %s" % url


class Test_url_lookup(unittest.TestCase):
    def setUp(self):
        self.service = url_lookup_service()
        self.service.setup()

        self.updated_urls = ['test_url1','test_url2']
        self.missing_urls = ['test_url3','test_url4']

        for url in self.updated_urls:
            self.service.db_obj.malware_db.add(url)

    def test_lookup_present(self):
        for url in self.updated_urls:
            assert (self.service.lookup_url(url)), "missing url %s" % url

    def test_lookup_absent(self):
        for url in self.missing_urls:
            assert (not self.service.lookup_url(url)), "extra url %s" % url

if __name__ == '__main__':
    unittest.main()
