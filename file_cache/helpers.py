import hashlib
import os
from file_cache.structures import CacheDefaults
from file_cache.exceptions import FileCacheException


def get_md5_checksum(path_to_file):
    """
    Return the MD5 checksum for file

    :param path_to_file:
    :return: MD5 checksum
    """
    with open(path_to_file, 'rb') as the_file:
        file_contents = the_file.read()
        return hashlib.md5(file_contents).digest()


def file_as_chunks(path_to_file: str, chunk_size: int)->list:
    """
    Convert a file to byte chunks and return those chunks as list

    :param path_to_file: Path to file
    :param chunk_size: Size (in bytes) of each chunk
    :return: list of chunks
    """
    chunks = []
    curr_bytes = None

    file_size = os.path.getsize(path_to_file)
    if file_size > CacheDefaults.MAX_FILE_SIZE.value:
        raise FileCacheException('File size too large')

    with open(path_to_file, 'rb') as the_file:
        empty_bytes = b''
        while curr_bytes != empty_bytes:
            curr_bytes = the_file.read(chunk_size)
            chunks.append(curr_bytes)

    return chunks
