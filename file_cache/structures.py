from enum import Enum


class CacheDefaults(Enum):
    HOST = 'localhost'
    PORT = 11211
    CHUNK_SIZE = 1024
    KEY_CHUNK = '{}_chunk_{}'
    KEY_CHECKSUM = '{}_checksum'
    KEY_NUMCHUNKS = '{}_chunk_count'
    MAX_FILE_SIZE = 50 * (1024**2)
