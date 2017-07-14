#
# coding: utf-8
#
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import xmlunittest
from lxml import etree

import pykml
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import get_factory_object_name
from pykml.factory import write_python_script_for_kml_document
from pykml.parser import Schema


class KmlFactoryTestCase(unittest.TestCase, xmlunittest.XmlTestMixin):
    def test_get_factory_object_name(self):
        """Tests obtaining a factory object"""
        self.assertEqual(
            get_factory_object_name('http://www.opengis.net/kml/2.2'),
            'KML'
        )
        self.assertEqual(
            get_factory_object_name('http://www.w3.org/2005/Atom'),
            'ATOM'
        )
        self.assertEqual(get_factory_object_name(None), 'KML')

    def test_trivial_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        doc = KML.kml()
        schema = Schema('ogckml22.xsd')
        self.assertTrue(schema.validate(doc))

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<kml xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2"/>'

        self.assertXmlEquivalentOutputs(data, expected)

    def test_basic_kml_document_2(self):
        """Tests the creation of a basic OGC KML document."""
        doc = KML.kml(
            KML.Document(
                KML.name('KmlFile'),
                KML.Placemark(
                    KML.name('Untitled Placemark'),
                    KML.Point(
                        KML.coordinates('-95.265,38.959,0')
                    )
                )
            )
        )
        # validate against a local schema
        self.assertTrue(Schema('ogckml22.xsd').validate(doc))
        # validate against a remote schema
        self.assertTrue(Schema('http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd').validate(doc))

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<kml xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2">' \
            b'<Document>' \
            b'<name>KmlFile</name>' \
            b'<Placemark>' \
            b'<name>Untitled Placemark</name>' \
            b'<Point>' \
            b'<coordinates>-95.265,38.959,0</coordinates>' \
            b'</Point>' \
            b'</Placemark>' \
            b'</Document>' \
            b'</kml>'

        self.assertXmlEquivalentOutputs(data, expected)

    def test_basic_kml_document(self):
        """Tests the creation of a basic KML with Google Extensions ."""
        doc = KML.kml(
            GX.Tour(
                GX.Playlist(
                    GX.SoundCue(
                        KML.href('http://dev.keyhole.com/codesite/cntowerfacts.mp3')
                    ),
                    GX.Wait(
                        GX.duration(10)
                    ),
                    GX.FlyTo(
                        GX.duration(5),
                        GX.flyToMode('bounce'),
                        KML.LookAt(
                            KML.longitude(-79.387),
                            KML.latitude(43.643),
                            KML.altitude(0),
                            KML.heading(-172.3),
                            KML.tilt(10),
                            KML.range(1200),
                            KML.altitudeMode('relativeToGround'),
                        )
                    )
                )
            )
        )
        self.assertTrue(Schema('kml22gx.xsd').validate(doc))

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<kml xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2">' \
            b'<gx:Tour>' \
            b'<gx:Playlist>' \
            b'<gx:SoundCue>' \
            b'<href>http://dev.keyhole.com/codesite/cntowerfacts.mp3</href>' \
            b'</gx:SoundCue>' \
            b'<gx:Wait>' \
            b'<gx:duration>10</gx:duration>' \
            b'</gx:Wait>' \
            b'<gx:FlyTo>' \
            b'<gx:duration>5</gx:duration>' \
            b'<gx:flyToMode>bounce</gx:flyToMode>' \
            b'<LookAt>' \
            b'<longitude>-79.387</longitude>' \
            b'<latitude>43.643</latitude>' \
            b'<altitude>0</altitude>' \
            b'<heading>-172.3</heading>' \
            b'<tilt>10</tilt>' \
            b'<range>1200</range>' \
            b'<altitudeMode>relativeToGround</altitudeMode>' \
            b'</LookAt>' \
            b'</gx:FlyTo>' \
            b'</gx:Playlist>' \
            b'</gx:Tour>' \
            b'</kml>'

        self.assertXmlEquivalentOutputs(data, expected)

    def test_kml_document_with_atom_element(self):
        """Tests the creation of a KML document with an ATOM element."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href='http://www.harrypotter.com'),
                KML.Placemark(
                    KML.name('Hogwarts'),
                    KML.Point(
                        KML.coordinates('1,1')
                    )
                )
            )
        )
        self.assertTrue(Schema('kml22gx.xsd').validate(doc))

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<kml xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2">' \
            b'<Document>' \
            b'<atom:author>' \
            b'<atom:name>J. K. Rowling</atom:name>' \
            b'</atom:author>' \
            b'<atom:link href="http://www.harrypotter.com"/>' \
            b'<Placemark>' \
            b'<name>Hogwarts</name>' \
            b'<Point>' \
            b'<coordinates>1,1</coordinates>' \
            b'</Point>' \
            b'</Placemark>' \
            b'</Document>' \
            b'</kml>'
        self.assertXmlEquivalentOutputs(data, expected)

    def test_kml_document_with_cdata_description(self):
        """Tests the creation of a KML document with a CDATA element."""
        doc = KML.description('<h1>CDATA Tags are useful!</h1>')

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<description ' \
            b'xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2">' \
            b'&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;' \
            b'</description>'

        self.assertXmlEquivalentOutputs(data, expected)

    def test_kml_document_with_cdata_description_2(self):
        """Tests the creation of a KML document with a CDATA element."""
        doc = KML.kml(
            KML.Document(
                KML.Placemark(
                    KML.name('CDATA example'),
                    KML.description(
                        '<h1>CDATA Tags are useful!</h1>'
                        '<p><font color="red">Text is <i>more readable</i> and '
                        '<b>easier to write</b> when you can avoid using entity '
                        'references.</font></p>'
                    ),
                    KML.Point(
                        KML.coordinates('102.595626,14.996729'),
                    ),
                ),
            ),
        )

        data = etree.tostring(doc, encoding='ascii')
        expected = \
            b'<kml xmlns:gx="http://www.google.com/kml/ext/2.2" ' \
            b'xmlns:atom="http://www.w3.org/2005/Atom" ' \
            b'xmlns="http://www.opengis.net/kml/2.2">' \
            b'<Document>' \
            b'<Placemark>' \
            b'<name>CDATA example</name>' \
            b'<description>' \
            b'&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;' \
            b'&lt;p&gt;&lt;font color="red"&gt;Text is &lt;i&gt;more readable&lt;/i&gt; and ' \
            b'&lt;b&gt;easier to write&lt;/b&gt; when you can avoid using entity ' \
            b'references.&lt;/font&gt;&lt;/p&gt;' \
            b'</description>' \
            b'<Point>' \
            b'<coordinates>102.595626,14.996729</coordinates>' \
            b'</Point>' \
            b'</Placemark>' \
            b'</Document>' \
            b'</kml>'

        self.assertXmlEquivalentOutputs(data, expected)


class GeneratePythonScriptTestCase(unittest.TestCase, xmlunittest.XmlTestMixin):
    def test_write_python_script_for_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name('J. K. Rowling')
                ),
                ATOM.link(href='http://www.harrypotter.com'),
                KML.Placemark(
                    KML.name('Hogwarts'),
                    KML.Point(
                        KML.coordinates('1,1')
                    )
                )
            )
        )
        script = write_python_script_for_kml_document(doc)
        expected = \
            'from lxml import etree\n' \
            'from pykml.factory import KML_ElementMaker as KML\n' \
            'from pykml.factory import ATOM_ElementMaker as ATOM\n' \
            'from pykml.factory import GX_ElementMaker as GX\n' \
            '\n' \
            'doc = KML.kml(\n' \
            '  KML.Document(\n' \
            '    ATOM.author(\n' \
            '      ATOM.name(\'J. K. Rowling\'),\n' \
            '    ),\n' \
            '    ATOM.link(href=\'http://www.harrypotter.com\',\n' \
            '),\n' \
            '    KML.Placemark(\n' \
            '      KML.name(\'Hogwarts\'),\n' \
            '      KML.Point(\n' \
            '        KML.coordinates(\'1,1\'),\n' \
            '      ),\n' \
            '    ),\n' \
            '  ),\n' \
            ')\n' \
            'print(etree.tostring(etree.ElementTree(doc), \n' \
            '                     encoding=\'utf-8\', \n' \
            '                     xml_declaration=True, \n' \
            '                     pretty_print=True).decode(\'utf-8\'))\n'

        self.assertEqual(script, expected)

    def test_write_python_script_for_multiline_coordinate_string(self):
        """Tests the creation of a trivial OGC KML document."""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'google_kml_reference' /
                         'altitudemode_reference.kml')
        with test_datafile.open('rb') as f:
            doc = pykml.parser.parse(f, schema=None)
        script = write_python_script_for_kml_document(doc)
        expected = \
            'from lxml import etree\n' \
            'from pykml.factory import KML_ElementMaker as KML\n' \
            'from pykml.factory import ATOM_ElementMaker as ATOM\n' \
            'from pykml.factory import GX_ElementMaker as GX\n' \
            '\n' \
            'doc = KML.kml(\n' \
            '  etree.Comment(\' required when using gx-prefixed elements \'),\n' \
            '  KML.Placemark(\n' \
            '    KML.name(\'gx:altitudeMode Example\'),\n' \
            '    KML.LookAt(\n' \
            '      KML.longitude(\'146.806\'),\n' \
            '      KML.latitude(\'12.219\'),\n' \
            '      KML.heading(\'-60\'),\n' \
            '      KML.tilt(\'70\'),\n' \
            '      KML.range(\'6300\'),\n' \
            '      GX.altitudeMode(\'relativeToSeaFloor\'),\n' \
            '    ),\n' \
            '    KML.LineString(\n' \
            '      KML.extrude(\'1\'),\n' \
            '      GX.altitudeMode(\'relativeToSeaFloor\'),\n' \
            '      KML.coordinates(\n' \
            '      \'146.825,12.233,400 \'\n' \
            '      \'146.820,12.222,400 \'\n' \
            '      \'146.812,12.212,400 \'\n' \
            '      \'146.796,12.209,400 \'\n' \
            '      \'146.788,12.205,400 \'\n' \
            '      ),\n' \
            '    ),\n' \
            '  ),\n' \
            ')\n' \
            'print(etree.tostring(etree.ElementTree(doc), \n' \
            '                     encoding=\'utf-8\', \n' \
            '                     xml_declaration=True, \n' \
            '                     pretty_print=True).decode(\'utf-8\'))\n'

        self.assertEqual(script, expected)

    def test_write_python_script_for_kml_document_with_cdata(self):
        """Tests the creation of an OGC KML document with a cdata tag"""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'google_kml_tutorial' /
                         'using_the_cdata_element.kml')
        schema = Schema('kml22gx.xsd')
        with test_datafile.open('rb') as f:
            doc = pykml.parser.parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)
        expected = \
            'from lxml import etree\n' \
            'from pykml.factory import KML_ElementMaker as KML\n' \
            'from pykml.factory import ATOM_ElementMaker as ATOM\n' \
            'from pykml.factory import GX_ElementMaker as GX\n' \
            '\n' \
            'doc = KML.kml(\n' \
            '  KML.Document(\n' \
            '    KML.Placemark(\n' \
            '      KML.name(\'CDATA example\'),\n' \
            '      KML.description(\n' \
            '          \'<h1>CDATA Tags are useful!</h1> \'\n' \
            '          \'<p><font color="red">Text is <i>more readable</i> and \'\n' \
            '          \'<b>easier to write</b> when you can avoid using entity \'\n' \
            '          \'references.</font></p> \'\n' \
            '      ),\n' \
            '      KML.Point(\n' \
            '        KML.coordinates(\'102.595626,14.996729\'),\n' \
            '      ),\n' \
            '    ),\n' \
            '  ),\n' \
            ')\n' \
            'print(etree.tostring(etree.ElementTree(doc), \n' \
            '                     encoding=\'utf-8\', \n' \
            '                     xml_declaration=True, \n' \
            '                     pretty_print=True).decode(\'utf-8\'))\n'

        self.assertEqual(script, expected)

        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            temp_python_file = f.name
            f.write(script)

        # execute the temporary python file to create a KML file

        current_env = os.environ.copy()
        current_env['PYTHONPATH'] = os.fspath(Path(__file__).parent.parent.parent)

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            exit_code = subprocess.call(['python', temp_python_file], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = pykml.parser.parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')

        os.unlink(temp_python_file)
        os.unlink(temp_kml_file)

    def test_write_python_script_for_kml_document_with_namespaces(self):
        """Tests the creation of an OGC KML document with several namespaces"""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'google_kml_developers_guide' /
                         'complete_tour_example.kml')
        schema = Schema('kml22gx.xsd')
        with test_datafile.open('rb') as f:
            doc = pykml.parser.parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)

        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            temp_python_file = f.name
            f.write(script)

        # execute the temporary python file to create a KML file
        # set the PYTHONPATH variable so that it references the root
        # of the pyKML library

        current_env = os.environ.copy()
        current_env['PYTHONPATH'] = os.fspath(Path(__file__).parent.parent.parent)

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            exit_code = subprocess.call(['python', temp_python_file], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = pykml.parser.parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')

        os.unlink(temp_python_file)
        os.unlink(temp_kml_file)

    def test_write_python_script_for_kml_document_with_comments(self):
        """Tests the creation of an OGC KML document with several comments"""
        test_datafile = (Path(__file__).parent /
                         'testfiles' /
                         'simple_file_with_comments.kml')
        schema = Schema('kml22gx.xsd')
        with test_datafile.open('rb') as f:
            doc = pykml.parser.parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)

        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            temp_python_file = f.name
            f.write(script)

        # execute the temporary python file to create a KML file

        current_env = os.environ.copy()
        current_env['PYTHONPATH'] = os.fspath(Path(__file__).parent.parent.parent)

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            exit_code = subprocess.call(['python', temp_python_file], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = pykml.parser.parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')
        # test that the original and generated documents are equivalent
        self.assertXmlEquivalentOutputs(etree.tostring(doc), etree.tostring(doc2))

        os.unlink(temp_python_file)
        os.unlink(temp_kml_file)


if __name__ == '__main__':
    unittest.main()
