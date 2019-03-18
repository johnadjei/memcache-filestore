import unittest
from file_cache.exceptions import (
    FileCacheException,
    FileCacheStoreException,
    FileCacheRetrieveException
)
from file_cache.models import FileCache
from file_cache.helpers import (
    get_md5_checksum,
    file_as_chunks,
    create_binary_file
)
from file_cache.structures import CacheDefaults
from unittest import mock
from pymemcache.client import Client as PyMemcacheClient
import os
import hashlib


class FileCacheTest(unittest.TestCase):
    cacher = None
    default_server = ('localhost', 11211)
    test_key_1 = 'test-key-1'
    test_key_2 = 'test-key-2'
    tmp_file = '/tmp/file.bin'
    tmp_file_text = b'This is a test'
    tmp_file_checksum = 'ce114e4501d2f4e2dcea3e17b546f339'
    tmp_file_big = '/tmp/file.big'
    tmp_file_bad = '/tmp/file.bad'
    tmp_file_oversize = '/tmp/file.toobig'
    max_file_size = CacheDefaults.MAX_FILE_SIZE.value
    max_chunks = CacheDefaults.MAX_FILE_SIZE_MB.value

    def setUp(self):
        self.cacher = FileCache()

    def tearDown(self):
        self.cacher.client.flush_all()
        self.cacher.client.close()


class TestHelpers(FileCacheTest):

    def setUp(self):
        super().setUp()
        with open(self.tmp_file, 'wb') as the_file:
            the_file.write(self.tmp_file_text)

    def tearDown(self):
        super().tearDown()
        if os.path.exists(self.tmp_file):
            os.unlink(self.tmp_file)
        if os.path.exists(self.tmp_file_big):
            os.unlink(self.tmp_file_big)
        if os.path.exists(self.tmp_file_oversize):
            os.unlink(self.tmp_file_oversize)

    def test_get_md5_checksum(self):
        test_chksum = get_md5_checksum(self.tmp_file)
        md5 = hashlib.md5(self.tmp_file_text).hexdigest()
        self.assertEqual(test_chksum, self.tmp_file_checksum)
        self.assertEqual(test_chksum, md5)

    def test_create_binary_file(self):
        # empty file
        with self.assertRaises(FileCacheException):
            create_binary_file(self.tmp_file, 0)

        # unsafe file
        with self.assertRaises(FileCacheException):
            create_binary_file('/root/file.secret', 1024)

        # normal file
        file_length = len(self.tmp_file_text)
        created = create_binary_file(self.tmp_file, file_length)
        self.assertTrue(created)

    def test_file_as_chunks(self):

        # ensure number of max chunks for max file size
        create_binary_file(self.tmp_file_big, self.max_file_size)
        chunks = file_as_chunks(self.tmp_file_big, 1024 ** 2)
        self.assertIsInstance(chunks, list)

        # filter out EOF or zero-byte
        chunks = list(filter(None, chunks))
        self.assertEqual(len(chunks), self.max_chunks)

        # bad file path
        with self.assertRaises(FileCacheException):
            file_as_chunks(self.tmp_file_bad, 1024**2)

        # file too big
        create_binary_file(self.tmp_file_oversize, self.max_file_size * 2)
        with self.assertRaises(FileCacheException):
            file_as_chunks(self.tmp_file_oversize, 1024 ** 2)


class TestFileCacheStore(FileCacheTest):

    def test_cacher_object(self):
        self.assertTrue(isinstance(self.cacher, FileCache))
        self.assertTrue(hasattr(self.cacher, 'store'))

    def test_client_object(self):
        self.assertTrue(isinstance(self.cacher.client, PyMemcacheClient))
        self.assertTrue(self.cacher.client.server == self.default_server)

    def test_store(self):
        fake_file_path = '/non/existent.file'
        # non-existent file
        with self.assertRaises(FileCacheStoreException):
            self.cacher.store(self.test_key_1, fake_file_path)

        # no key provided
        with self.assertRaises(FileCacheStoreException):
            self.cacher.store(None, fake_file_path)

        # temp file 1kb
        create_binary_file(self.tmp_file, 1024)
        stored = self.cacher.store(self.test_key_1, self.tmp_file)
        self.assertTrue(stored)

        # oversize file, max size + 1kb
        create_binary_file(self.tmp_file_oversize, self.max_file_size + 1024)
        with self.assertRaises(FileCacheStoreException):
            self.cacher.store(self.test_key_1, self.tmp_file_oversize)

        # file already cached
        create_binary_file(self.tmp_file_big, 10 * (1024**2))
        stored_1 = self.cacher.store(self.test_key_2, self.tmp_file_big)
        self.assertTrue(stored_1)
        # with self.assertRaises(FileCacheStoreException):
        #     self.cacher.store(self.test_key_1 + '2', self.tmp_file)


# class TestFileCacheStore(unittest.TestCase):
#
#     cacher = None
#     default_server = ('localhost', 11211)
#
#     def setUp(self):
#         self.cacher = FileCache()
#
#     def tearDown(self):
#         self.cacher.client.flush_all()
#         self.cacher.client.close()
#
#     def test_cacher_object(self):
#         self.assertTrue(isinstance(self.cacher, FileCache))
#         self.assertTrue(hasattr(self.cacher, 'store'))
#         self.assertTrue(hasattr(self.cacher, 'retrieve'))
#
#     def test_client_object(self):
#         self.assertTrue(isinstance(self.cacher.client, PyMemcacheClient))
#         self.assertTrue(self.cacher.client.server == self.default_server)
#
#     def test_2(self):
#         with self.assertRaises(FileCacheStoreException):
#             path_to_file = '/Users/john/Downloads//Ntrepid_Prescreen_Form_Nov_2017.pdf'

        # pass

    # def test_store_no_file(self):
    #     path_to_file = '/tmp/'
    #
    # def test_store_large_file(self):
    #     self.assertTrue(True)


# class TestFileCacheRetrieve(unittest.TestCase):
#
#     def test_retrieve_no_file(self):
#         self.assertTrue(True)
#
#     def test_retrieve_large_file(self):
#         self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
