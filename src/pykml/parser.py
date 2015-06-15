#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
"""pyKML Parser Module

The pykml.parser module provides functions that can be used to parse KML 
from a file or remote URL.
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import os
import ssl
from lxml import etree, objectify
from six.moves.urllib.request import urlopen

OGCKML_SCHEMA = 'http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd'


class Schema():
    """A class representing an XML Schema used to validate KML documents"""

    def __init__(self, schema):
        try:
            module_dir = os.path.split(__file__)[0]  # get the module path
            schema_file = os.path.join(module_dir, "schemas", schema)
            # try to open a local file
            with open(schema_file, 'rb') as f:
                self.schema = etree.XMLSchema(file=f)
        except:
            # try to open a remote URL
            context = ssl._create_unverified_context()
            f = urlopen(schema, context=context)
            self.schema = etree.XMLSchema(file=f)

    def validate(self, doc):
        """Validates a KML document
        
        This method eturns a boolean value indicating whether the KML document 
        is valid when compared to the XML Schema."""
        return self.schema.validate(doc)

    def assertValid(self, doc):
        """Asserts that a KML document is valide
        
        The method generates a validation error if the document is not valid
        when compared to the XML Schema.
        """
        return self.schema.assertValid(doc)


def _parse_internal(source, parse_func, schema=None, parser_options=None):
    _parser_options = {
        'strip_cdata': False,
    }
    if parser_options:
        _parser_options.update(parser_options)

    if schema:
        _parser_options['schema'] = schema.schema

    parser = objectify.makeparser(**_parser_options)
    return parse_func(source, parser=parser)


def fromstring(text, schema=None, parser_options=None):
    """Parses a KML text string
    
    This function parses a KML text string and optionally validates it against 
    a provided schema object"""

    return _parse_internal(text, objectify.fromstring, schema, parser_options)


def parse(fileobject, schema=None, parser_options=None):
    """Parses a file object
    
    This function parses a KML file object, and optionally validates it against 
    a provided schema.
    """
    return _parse_internal(fileobject, objectify.parse, schema, parser_options)


def validate_kml():
    """Validate a KML file
    
    Example: validate_kml test.kml
    """
    from pykml.parser import parse
    from optparse import OptionParser

    parser = OptionParser(
        usage="usage: %prog FILENAME_or_URL",
        version="%prog 0.1",
    )
    parser.add_option("--schema", dest="schema_uri",
                      help="URI of the XML Schema Document used for validation")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of arguments")
    else:
        uri = args[0]

    try:
        # try to open as a file
        fileobject = open(uri, 'rb')
    except IOError:
        try:
            fileobject = urlopen(uri)
        except ValueError:
            raise ValueError('Unable to load URI {0}'.format(uri))
    except:
        raise

    doc = parse(fileobject, schema=None)

    if options.schema_uri:
        schema = Schema(options.schema_uri)
    else:
        # by default, use the OGC base schema
        sys.stdout.write("Validating against the default schema: {0}\n".format(OGCKML_SCHEMA))
        schema = Schema(OGCKML_SCHEMA)

    sys.stdout.write("Validating document...\n")
    if schema.validate(doc):
        sys.stdout.write("Congratulations! The file is valid.\n")
    else:
        sys.stdout.write("Uh-oh! The KML file is invalid.\n")
        sys.stdout.write(schema.assertValid(doc))
    # close the fileobject, if needed
    try:
        fileobject
    except NameError:
        pass  # variable was not defined
    else:
        fileobject.close()
