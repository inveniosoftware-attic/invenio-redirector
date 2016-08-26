# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module that adds custom redirection handlers."""

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

requirements = [
    'Flask>=0.11.1',
    'six>=1.7.2',
    'invenio-base>=0.2.1',
    'invenio-ext>=0.1.0',
    'invenio-utils>=0.1.0',
]

test_requirements = [
    'pytest>=2.8.0',
    'pytest-cov>=2.1.0',
    'pytest-pep8>=1.0.6',
    'coverage>=4.0.0',
]

setup_requires = [
    'pytest-runner>=2.6.2',
]

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_redirector', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-redirector',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='GPLv2',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-redirector',
    packages=[
        'invenio_redirector',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'gotoadmin = invenio_redirector.scripts.redirector:main',
        ],
    },
    install_requires=requirements,
    extras_require={
        'docs': [
            'Sphinx>=1.3',
            'sphinx_rtd_theme>=0.1.7'
        ],
        'tests': test_requirements
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
    ],
    tests_require=test_requirements,
)
