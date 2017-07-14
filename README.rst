PyKML
=====
PyKML is a Python package for authoring, parsing, and manipulating KML
documents.  It is based on the lxml_ library which provides a Python API for
working with XML documents.

This Fork (work in progress)
----------------------------
This repository is a fork of https://github.com/shabble/pykml. This fork
supports Python 3.6 only as tested on Microsoft Windows. The
original supported Python 2.x only.

xmlunittest_ is used for the XML unittests as the original repository's
lexographical comparison of XML is not consistent across Python
implementations.

The original documentation is better. For the original documentation see
https://pythonhosted.org/pykml/ - there are no API changes in this fork - just
remember that XML documents are *bytes* in Python 3.x

Dependencies
------------
* lxml_ (>=2.2.8, older versions not tested)
* xmlunittest_ (for xml unittests)

.. _lxml: http://lxml.de
.. _xmlunittest: https://pypi.python.org/pypi/xmlunittest

Installation
------------
To install this port:

* install the dependencies
* download this repository and do the usual ``python setup.py install``
