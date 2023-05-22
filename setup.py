#!/usr/bin/env python
# encoding: utf-8

import io
import os
import sys
import codecs
from shutil import rmtree

from setuptools import find_packages, setup, Command


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

required = [
    'requests==2.31.0',
    'beautifulsoup4==4.6.0',
    'pymongo==3.6.1'

]

version = '1.0'

setup(
    name='TOP205IMDB',
    version=version,
    description='scrape all top 250 moives list from IMDB',
    long_description=long_description,
    author='Matar',
    author_email='matar@linux.com',
    url='https://github.com/mataralhawiti/Top250IMDB',
    install_requires=required,
    license='GPL v3',
    classifiers=(
        'Development Status :: dev',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL v3 License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)