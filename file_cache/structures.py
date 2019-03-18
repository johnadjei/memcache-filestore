from enum import Enum


class CacheDefaults(Enum):
    HOST = 'localhost'
    PORT = 11211
    CHUNK_SIZE = 1024**2
    KEY_CHUNK = '{}_chunk_{}'
    KEY_CHECKSUM = 'file_{}'
    KEY_NUMCHUNKS = '{}_chunk_count'
    MAX_FILE_SIZE_MB = 50
    MAX_FILE_SIZE = MAX_FILE_SIZE_MB * (1024**2)
