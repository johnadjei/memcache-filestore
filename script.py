import argparse
from file_cache.exceptions import (
    FileCacheStoreException,
    FileCacheException,
    FileCacheRetrieveException
)
from file_cache.models import FileCache
import io


def store(name, infile):
    # call your library here
    cache_client = FileCache()
    return cache_client.store(name, infile)


def retrieve(name, outfile):
    # call your library here
    cache_client = FileCache()
    return cache_client.retrieve(name, outfile)


def main():
    """ Process Command Line Arguments """
    parser = argparse.ArgumentParser(description='Store and retrieve files in Memcached')
    parser.add_argument('action', help='Action to process (store, retrieve)')
    parser.add_argument('name', help='Name of the file')
    parser.add_argument('file', help='File for processing')

    try:
        args = parser.parse_args()
        if args.action == 'store':
            store(args.name, args.file)
        elif args.action == 'retrieve':
            ret_bytes = io.BytesIO(retrieve(args.name, args.file))
            # print(ret_bytes.read())
        else:
            parser.print_help()
    except (FileCacheStoreException, FileCacheRetrieveException,
            FileCacheException) as exc:
        print(str(exc))
        exit(1)


if __name__ == "__main__":
    main()
