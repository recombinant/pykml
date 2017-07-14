#
# coding: utf-8
#
import ssl
import unittest
from io import BytesIO
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from lxml import etree

from pykml.parser import Schema
from pykml.parser import fromstring
from pykml.parser import parse


class ValidatorTestCase(unittest.TestCase):
    def test_initialize_schema(self):
        """Tests the creation Schema instance"""
        schema = Schema("ogckml22.xsd")
        self.assertTrue(isinstance(schema.schema, etree.XMLSchema))

    def test_initialize_schema_remote_url(self):
        schema = Schema('https://developers.google.com/kml/schema/kml22gx.xsd')
        self.assertTrue(isinstance(schema.schema, etree.XMLSchema))


class ParseKmlOgcTestCase(unittest.TestCase):
    """A collection of tests related to parsing KML OGC documents"""

    def test_fromstring_kml_document(self):
        """Tests the parsing of an valid KML string"""
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'.encode('ascii')
        tree = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
        self.assertEqual(etree.tostring(tree, encoding='ascii'), test_kml)
        tree = fromstring(test_kml)
        self.assertEqual(etree.tostring(tree, encoding='ascii'), test_kml)

    def test_fromstring_invalid_kml_document(self):
        """Tests the parsing of an invalid KML string"""
        test_kml = b'<bad_element />'
        with self.assertRaises(etree.XMLSyntaxError):
            # tree =
            fromstring(test_kml, schema=Schema("ogckml22.xsd"))

    def test_parse_kml_document(self):
        """Tests the parsing of an valid KML file object"""
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'.encode('ascii')
        fileobject = BytesIO(test_kml)
        schema = Schema("ogckml22.xsd")
        tree = parse(fileobject, schema=schema)
        self.assertEqual(etree.tostring(tree), test_kml)
        tree = parse(fileobject, schema=schema)
        self.assertEqual(etree.tostring(tree), test_kml)

    def test_parse_invalid_kml_document(self):
        """Tests the parsing of an invalid KML document"""
        fileobject = BytesIO('<bad_element />'.encode('ascii'))
        with self.assertRaises(etree.XMLSyntaxError):
            # tree =
            parse(fileobject, schema=Schema("ogckml22.xsd"))

    def test_parse_kml_url(self):
        """Tests the parsing of a KML URL"""
        url = 'https://developers.google.com/kml/documentation/KML_Samples.kml'
        # url = 'http://kml-samples.googlecode.com/svn/trunk/kml/Document/doc-with-id.kml'
        # url = 'https://developers.google.com/kml/documentation/kmlfiles/altitudemode_reference.kml'
        # url = 'https://developers.google.com/kml/documentation/kmlfiles/animatedupdate_example.kml'
        context = ssl._create_unverified_context()
        try:
            with urlopen(url, context=context) as fileobject:
                tree = parse(fileobject, schema=Schema("ogckml22.xsd"))

            tree_string = etree.tostring(tree, encoding='ascii')[:78]
            expected_string = \
                b'<kml xmlns="http://www.opengis.net/kml/2.2">' \
                b'<Document>' \
                b'<name>KML Samples</name>'

            self.assertEqual(tree_string, expected_string)

        except URLError:
            print('Unable to access the URL. Skipping test...')

    def test_parse_kml_file_with_cdata(self):
        """Tests the parsing of a local KML file, with a CDATA description string"""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'google_kml_tutorial' /
                         'using_the_cdata_element.kml')
        # parse with validation
        with test_datafile.open('rb') as f:
            doc = parse(f, schema=Schema('ogckml22.xsd'))
        doc1_string = etree.tostring(doc, encoding='ascii')
        expected_string = \
            b'<kml xmlns="http://www.opengis.net/kml/2.2">' \
            b'<Document>' \
            b'<Placemark>' \
            b'<name>CDATA example</name>' \
            b'<description>' \
            b'<![CDATA[\n' \
            b'          <h1>CDATA Tags are useful!</h1>\n' \
            b'          <p><font color="red">Text is <i>more readable</i> and \n' \
            b'          <b>easier to write</b> when you can avoid using entity \n' \
            b'          references.</font></p>\n' \
            b'        ]]>' \
            b'</description>' \
            b'<Point>' \
            b'<coordinates>102.595626,14.996729</coordinates>' \
            b'</Point>' \
            b'</Placemark>' \
            b'</Document>' \
            b'</kml>'
        self.assertEqual(doc1_string, expected_string)

        # parse without validation
        with test_datafile.open('rb') as f:
            doc2 = parse(f)
        doc2_string = etree.tostring(doc2)
        self.assertEqual(doc2_string, expected_string)

    def test_parse_invalid_ogc_kml_document(self):
        """Tests the parsing of an invalid KML document.  Note that this KML
        document uses elements that are not in the OGC KML spec.
        """
        url = 'https://developers.google.com/kml/documentation/kmlfiles/altitudemode_reference.kml'
        context = ssl._create_unverified_context()
        try:
            with urlopen(url, context=context) as fileobject:
                with self.assertRaises(etree.XMLSyntaxError):
                    # tree =
                    parse(fileobject, schema=Schema("ogckml22.xsd"))

        except URLError:
            print('Unable to access the URL. Skipping test...')


class ParseKmlGxTestCase(unittest.TestCase):
    """A collection of tests related to parsing KML Google Extension documents"""

    def test_parse_kml_url(self):
        """Tests the parsing of a KML URL"""
        url = 'https://developers.google.com/kml/documentation/kmlfiles/altitudemode_reference.kml'
        context = ssl._create_unverified_context()
        try:
            with urlopen(url, context=context) as fileobject:
                tree = parse(fileobject, schema=Schema('kml22gx.xsd'))

            tree_string = etree.tostring(tree, encoding='ascii')[:185]
            expected_string = \
                b'<kml xmlns="http://www.opengis.net/kml/2.2" ' \
                b'xmlns:gx="http://www.google.com/kml/ext/2.2">' \
                b'<!-- required when using gx-prefixed elements -->' \
                b'<Placemark>' \
                b'<name>gx:altitudeMode Example</name>'

            self.assertEqual(tree_string, expected_string)

        except URLError:
            print('Unable to access the URL. Skipping test...')

    def test_parse_kml_file(self):
        """Tests the parsing of a local KML file, with validation"""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'google_kml_developers_guide' /
                         'complete_tour_example.kml')
        # parse without validation
        with test_datafile.open('rb') as f:
            # doc =
            parse(f)
        # parse with validation (local schema file)
        with test_datafile.open('rb') as f:
            # doc =
            parse(f, schema=Schema('kml22gx.xsd'))
        # parse with validation (remote schema file)
        with test_datafile.open('rb') as f:
            # doc =
            parse(f, schema=Schema('https://developers.google.com/kml/schema/kml22gx.xsd'))
        self.assertTrue(True)

    def test_parse_kml_url_2(self):
        """Tests the parsing of a KML URL"""
        url = 'https://developers.google.com/kml/documentation/kmlfiles/animatedupdate_example.kml'
        context = ssl._create_unverified_context()
        try:
            with urlopen(url, context=context) as fileobject:
                tree = parse(fileobject, schema=Schema('kml22gx.xsd'))

            tree_string = etree.tostring(tree, encoding='ascii')[:137]
            expected_string = \
                b'<kml xmlns="http://www.opengis.net/kml/2.2" ' \
                b'xmlns:gx="http://www.google.com/kml/ext/2.2">' \
                b'<Document>' \
                b'<name>gx:AnimatedUpdate example</name>'

            self.assertEqual(tree_string, expected_string)

        except URLError:
            print('Unable to access the URL. Skipping test...')


if __name__ == '__main__':
    unittest.main()
