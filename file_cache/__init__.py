from pymemcache.client.base import Client
from enum import Enum
import hashlib
import os



class FileCacheException(Exception):
    pass


class FileCacheStoreException(FileCacheException):
    pass


class FileCacheRetrieveException(FileCacheException):
    pass


class CacheDefaults(Enum):
    HOST = 'localhost'
    PORT = 11211
    CHUNK_SIZE = 1024
    KEY_CHUNK = '{}_chunk_{}'
    KEY_CHECKSUM = '{}_checksum'


class FileCache(object):
    """
    - Your library should be small and self contained.
    - Your library should use pymemcache or similar memcached client, along with the Python standard library, and any other resources.
    - Your library should accept any file size from 0 to 50MB. Files larger than 50MB should be rejected.
    - Your library should accept a file, chunk it, and store as bytes in Memcached with a minimum amount of overhead.
    - Your library should retrieve a file's chunks from Memcached and return a single stream of bytes.
    - Your library may chunk the file in any way appropriate.
    - Your library can key the chunks in any way appropriate.
    - Your library should check for file consistency to ensure the data retrieved is the same as the original data stored.
    - Your library should handle edge cases appropriately by raising an Exception or similar. Some examples of edge cases may include: trying to store a file that already exists, trying to retrieve a file that does not exist, or when a file retrieved is inconsistent/corrupt.
    - Your library should have at least two tests.
    """
    client = None

    def __init__(self, host='', port=0):
        """
        Initialize a FileCache object and connect the client via pymemcache
        :param host: Memcached server
        :param port: Memcached port
        """
        if not host:
            host = CacheDefaults.HOST.value
        if not port:
            port = CacheDefaults.PORT.value

        self.client = Client((host, port))

    def _get_md5_checksum(self, path_to_file):
        """
        Return the MD5 checksum for file

        :param path_to_file:
        :return: MD5 checksum
        """
        with open(path_to_file, 'rb') as the_file:
            file_contents = the_file.read()
            return hashlib.md5(file_contents).digest()

    def _file_as_chunks(self, path_to_file: str, chunk_size: int)->list:
        """
        Convert a file to byte chunks and return those chunks as list

        :param path_to_file: Path to file
        :param chunk_size: Size (in bytes) of each chunk
        :return: list of chunks
        """
        chunks = []
        curr_bytes = None

        with open(path_to_file, 'rb') as the_file:
            empty_bytes = b''
            while curr_bytes != empty_bytes:
                curr_bytes = the_file.read(chunk_size)
                chunks.append(curr_bytes)

        return chunks

    def _store_file(self, key: str, chunks: list, checksum: str)->bool:
        """
        Store a file into the cache as chunks using a key

        :param key:
        :param chunks:
        :param checksum:
        :return: boolean True on success
        """
        # raise exception if file already exists by checking
        # to see if checksum for this key has already been cached
        if self.client.get(CacheDefaults.KEY_CHECKSUM.value):
            raise FileCacheStoreException('Key/file already exists')

        self.client.set(CacheDefaults.KEY_CHECKSUM.value, checksum)

        # iterate over each chunk and cache that piece
        for k, curr_chunk in enumerate(chunks):
            curr_key = CacheDefaults.KEY_CHUNK.value.format(key, k)
            self.client.set(curr_key, curr_chunk)

        return True

    def _retrieve_file(self, key, path_to_outfile):

        # reconstitute the checksum by retrieving it from cache
        checksum = self.client.get(CacheDefaults.KEY_CHECKSUM.value.format(key))


    def store(self, key, path_to_file)->bool:
        """
        Store a file with a key

        :param key: Name of key to store in cache
        :param path_to_file: Path of file to store in cache
        :return: boolean True on success or raise exception
        """

        # ensure that key is provided
        if not key:
            raise FileCacheStoreException('Key not provided')

        # ensure that file exists
        if not os.path.exists(path_to_file):
            raise FileCacheStoreException('File does not exist')

        checksum = self._get_md5_checksum(path_to_file)
        chunks = self._file_as_chunks(path_to_file,
                                      CacheDefaults.CHUNK_SIZE.value)

        return self._store_file(key, chunks, checksum)

    def retrieve(self, key, path_to_outfile)->bytes:

        # ensure that key is provided
        if not key:
            raise FileCacheRetrieveException('Key not provided')

        """
        To implement this successfully, I'd need to get the list of chunks 
        based on the key and reconstitute them (in order) by joining them 
        back together into one blob and return. No time! :(
        """

        return None
