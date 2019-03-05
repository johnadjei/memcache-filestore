import pymemcache


class FileCacheException(Exception):
    pass


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
    def __init__(self):
        pass

