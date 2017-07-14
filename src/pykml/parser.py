#
# coding: utf-8
#
# pykml.parser
#
"""
The pykml.parser module provides functions that can be used to parse KML 
from a file or remote URL.
"""
import ssl
from contextlib import closing
from optparse import OptionParser
from pathlib import Path
from urllib.request import urlopen

from lxml import etree, objectify

from . import version as pykml_version

OGCKML_SCHEMA = 'http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd'


class Schema:
    """A class representing an XML Schema used to validate KML documents"""

    def __init__(self, schema):
        # TODO: use requests, open local file, open module dir file
        try:
            schema_file = Path(__file__).parent / 'schemas' / schema
            # try to open a local file
            with schema_file.open('rb') as f:
                self.schema = etree.XMLSchema(file=f)
        except:
            # try to open a remote URL
            context = ssl._create_unverified_context()
            with closing(urlopen(schema, context=context)) as f:
                self.schema = etree.XMLSchema(file=f)

    def validate(self, doc):
        """Validates a KML document

        This method returns a boolean value indicating whether the KML document
        `doc` is valid when compared to the XML Schema."""
        return self.schema.validate(doc)

    def assertValid(self, doc):
        """Asserts that a KML document is valid

        The method raises a validation exception if the document `doc` is not
        valid when compared to the XML Schema.
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
    from .util import open_pykml_uri

    parser = OptionParser(
        usage='usage: %prog FILENAME_or_URL',
        version=f'%prog {pykml_version}',
    )
    parser.add_option('--schema', dest='schema_uri',
                      help='URI of the XML Schema Document used for validation')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('wrong number of arguments')
    else:
        uri = args[0]

    with open_pykml_uri(uri, mode='rb') as f:
        try:
            print(f'Parsing "{uri}"')
            doc = parse(f, schema=None)

        except etree.XMLSyntaxError as e:
            print(f'Invalid XML: {e.msg}')
            exit(1)

    # load the schema
    if options.schema_uri:
        schema = Schema(options.schema_uri)
    else:
        # by default, use the OGC base schema
        print(f'Validating against the default schema: {OGCKML_SCHEMA}')
        schema = Schema(OGCKML_SCHEMA)

    print('Validating document...')
    try:
        schema.assertValid(doc)
        print('Congratulations! The file is valid.')

    except etree.DocumentInvalid as e:
        print('Uh-oh! The KML file is invalid.')
        for line in e.args:
            print(line)
