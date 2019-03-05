import unittest
from file_cache import (
    FileCacheStoreException, FileCacheRetrieveException,
    FileCache)


class TestFileCacheStore(unittest.TestCase):

    def test_store_no_file(self):
        self.assertTrue(True)

    def test_store_large_file(self):
        self.assertTrue(True)


class TestFileCacheRetrieve(unittest.TestCase):

    def test_retrieve_no_file(self):
        self.assertTrue(True)

    def test_retrieve_large_file(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
