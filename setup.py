#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py
import os
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

packages = ['memcache_filestore']
requires = ['pymemcache>=2.1.1']
test_requirements = ['pytest-cov', 'pytest-mock', 'pytest>=2.8.0']

about = {}
with open(os.path.join(here, 'memcache_filestore', '__version__.py'),
          'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE'], 'memcache_filestore': ['*.pem']},
    package_dir={'memcache_filestore': 'memcache_filestore'},
    include_package_data=True,
    python_requires=">=3.4",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    extras_require={},
)