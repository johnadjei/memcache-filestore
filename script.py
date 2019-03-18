import argparse
from file_cache.exceptions import (
    FileCacheStoreException,
    FileCacheException,
    FileCacheRetrieveException
)
from file_cache.models import FileCache


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
            retrieve(args.name, args.file)
        else:
            parser.print_help()
    except (FileCacheStoreException, FileCacheRetrieveException,
            FileCacheException) as exc:
        print(str(exc))
        exit(1)
    except Exception as exc:
        print(str(exc))
        exit(2)


if __name__ == "__main__":
    main()
