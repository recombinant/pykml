#
# coding: utf-8
#
# To create wheel use:
# python.exe setup.py install bdist_wheel --universal
#
import os
from os import sys

from setuptools import setup

sys.path.append(os.path.abspath('./src'))
from pykml import version


setup(
    name='pykml',
    version=version,
    packages=['pykml', ],
    package_dir={'': 'src'},
    package_data={
        'pykml': [
            'schemas/*.xsd',
        ],
    },
    install_requires=[
        'lxml>=3.8.0', 'requests>2.18.0', 'pytest-runner',
    ],
    tests_require=[
        'pytest', 'xmlunittest',
    ],
    description="Python KML library",
    classifiers=[
        # Get strings from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='kml',
    author='Tyler Erickson',
    author_email='tylerickson@gmail.com',
    url='https://pypi.python.org/pypi/pykml',
    license='BSD',
    long_description="""\
=========
pyKML
=========
pyKML is a Python package for parsing and authoring KML documents. It is based
on the lxml.objectify API (http://lxml.de/objectify.html) which
provides Pythonic access to XML documents.

.. figure:: https://github.com/shabble/pykml/blob/master/docs/source/logo/pyKML_logo_200x200.png
   :scale: 100 %
   :alt: pyKML logo

See the Package Documentation for information on installation and usage.
""",
    entry_points={
        'console_scripts': [
            'kml2pykml = pykml.factory:kml2pykml',
            'csv2kml = pykml.util:csv2kml',
            'validate_kml = pykml.parser:validate_kml',
        ],
    }
)
