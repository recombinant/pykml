PyKML
=====
PyKML is a Python package for authoring, parsing, and manipulating KML
documents.  It is based on the lxml_ library which provides a Python API for
working with XML documents.

This Fork
---------
This repository is a fork of https://github.com/shabble/pykml. This fork
supports Python 2.7, 3.4 & 3.5 as tested on Microsoft Windows. The 
original supports Python 2.x only (as of July 2015)

The working code and unittests were made compatible with Python 3.4 using six_
and xmlunittest_. The biggest change being that all XML documents are now
*bytes* in Python 3.x but *strings* in Python 2.7 - confusing for the
unsuspecting. xmlunittest_ is used for the XML unittests as the original port's
lexographical comparison is not consistent across Python implementations.

The documentation in this fork is work in progress. The original documentation
is better.

For the original documentation see https://pythonhosted.org/pykml/ - there are
no functional changes in this fork - just remember that XML documents are *bytes*
in Python 3.x

Dependencies
------------
* lxml_ (>=2.2.8, older versions not tested)
* xmlunittest_ (for xml unittests)
* six_ (Python 2 and 3 compatibility utilities)

.. _lxml: http://lxml.de
.. _xmlunittest: https://pypi.python.org/pypi/xmlunittest
.. _six: https://pypi.python.org/pypi/six

Installation
------------
To install this port:

* install the dependencies
* download this repository and do the usual ``python setup.py install``
