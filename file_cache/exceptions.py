class FileCacheException(Exception):
    pass


class FileCacheStoreException(FileCacheException):
    pass


class FileCacheRetrieveException(FileCacheException):
    pass
