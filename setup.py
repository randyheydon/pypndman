#!/usr/bin/env python2
from distutils.core import setup

setup(
    name = 'pypndman',
    version = '0.0.0',
    description = 'A Python wrapper around libpndman.',
    long_description = open('README.rst').read(),
    author = 'Randy Heydon',
    author_email = 'randy.heydon@clockworklab.net',
    url = 'https://github.com/Tempel/pypndman',
    packages = ['pndman'],
    license = '??',
)
