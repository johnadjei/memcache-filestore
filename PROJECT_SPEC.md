# Zapier Backend Engineering Skills Interview

## Project Details

Please consider this document as a set of requirements, and deliver the code necessary to fulfill these requirements. If a requirement seems ambiguous, state your understanding of the requirements in a readme or inline comments along with your solution.

## Scenario

Your mission is to write a Python library that will accept a large file (50MB) as an input and store it in Memcache. Once stored, the library will then be used to retrieve the file from Memcache and return it.

---

You might be asking "what's the catch?" 

Well, using the default slab size, Memcached can only store up to 1MB per key. That means you'll have to implement some means of chunking the file to store it in Memcached.

Further, Memcached can evict keys when it runs out of memory. A complete solution should detect these cases and handle them appropriately.

## Deliverables

There are three deliverables for this project:

1. A small library to store and retrieve large files in Memcached
2. At set of unit tests to validate the store and retrieve functionality
3. A command line utility (example below) to store and retrieve the files using your library

## Specs

### Library:

* Your library should be small and self contained.
* Your library should use `pymemcache` or similar memcached client, along with the Python standard library, and any other resources.
* Your library should accept any file size from 0 to 50MB. Files larger than 50MB should be rejected.
* Your library should accept a file, chunk it, and store as bytes in Memcached with a minimum amount of overhead. 
* Your library should retrieve a file's chunks from Memcached and return a single stream of bytes. 
* Your library may chunk the file in any way appropriate.
* Your library can key the chunks in any way appropriate.
* Your library should check for file consistency to ensure the data retrieved is the same as the original data stored.
* Your library should handle edge cases appropriately by raising an Exception or similar. Some examples of edge cases may include: trying to store a file that already exists, trying to retrieve a file that does not exist, or when a file retrieved is inconsistent/corrupt. 
* Your library should have at least two tests.

**NOTE:** you can use this command to generate a 50MB file of random data if needed:

```bash
dd if=/dev/urandom of=bigoldfile.dat bs=1048576 count=50
```

### Command Line Utility

* Your command line utility should use this code as a starting point:

```python
import argparse


def store(name, infile):
    # call your library here
    pass


def retrieve(name, outfile):
    # call your library here
    pass


def main():
    """ Process Command Line Arguments """
    parser = argparse.ArgumentParser(description='Store and retrieve files in Memcached')
    parser.add_argument('action', help='Action to process (store, retrieve)')
    parser.add_argument('name', help='Name of the file')
    parser.add_argument('file', help='File for processing')

    args = parser.parse_args()
    if args.action == 'store':
        store(args.name, args.file)
    elif args.action == 'retrieve':
        retrieve(args.name, args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

Example Store:
`python script.py store bigfile bigoldfile.dat`

Example Retrieve:
`python script.py retrieve bigfile newbigoldfile.dat`


## How we'll review your code:

We did this project ourselves so we should have a good time comparing versions. Once complete, we'll be reviewing your code for:

* **Completeness** - Did you complete an implementation that meets the spec?
* **Correctness** - Does your solution perform the correct functionality? (i.e., Does it work when we run it?)
* **Clarity** - Can we understand your code and the decisions you made in the implementation?
* **Code Quality** - Is your code well structured and clean? Does it use common idioms? Does it adhere to PEP8?

## Project time limit:

Please do not spend more than **2.5 hours** on the project.

It's a good idea to wrap things up early and have time for cleanup, **even if that means that all features aren't complete**. Code quality and completeness will both be considered. Completing the project in less time than the time limit may improve your score, but only marginally. Code and app quality will be weighted a lot more, so use the time to your best ability.

Be sure to commit your code regularly as you work through your solution. This is helpful for us to understand how you work. At the very least, you must commit and push to GitHub once during the project or we will not be able to score your solution.

**Commits after the time limit will not be scored.** Go over time? Don't worry! Wrap up and commit what you've got. We will still review everything up to the limit.

## Once finished

* To deliver your project, simply commit your final work and push to the `project` branch of the private Github repo provided by Zapier. 

* Open a pull request to merge your `project` branch to `master`. Time spent opening up the pull request will **not** count as part of your project time, but please make sure to open the pull request within (roughly) one hour after your final commit.

  * Make sure to add a description to your pull request with any details you want to provide.

  * At the very least, It is useful to provide a description of how to run your project.

* If you finish early and want to submit unfinished ideas, please add those to other branches.
