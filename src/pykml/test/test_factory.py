#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import os
from os import path
import tempfile
import subprocess

import xmlunittest

from lxml import etree
import six

from pykml.parser import Schema
from pykml.parser import parse
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from pykml.factory import get_factory_object_name
from pykml.factory import write_python_script_for_kml_document


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
        schema = Schema("ogckml22.xsd")
        self.assertTrue(schema.validate(doc))
        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
              'xmlns:atom="http://www.w3.org/2005/Atom" '
              'xmlns="http://www.opengis.net/kml/2.2"/>'
            ).encode('ascii')
        )

    def test_basic_kml_document_2(self):
        """Tests the creation of a basic OGC KML document."""
        doc = KML.kml(
            KML.Document(
                KML.name("KmlFile"),
                KML.Placemark(
                    KML.name("Untitled Placemark"),
                    KML.Point(
                        KML.coordinates("-95.265,38.959,0")
                    )
                )
            )
        )
        # validate against a local schema
        self.assertTrue(Schema("ogckml22.xsd").validate(doc))
        # validate against a remote schema
        self.assertTrue(Schema("http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd").validate(doc))

        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<name>KmlFile</name>'
                '<Placemark>'
                  '<name>Untitled Placemark</name>'
                  '<Point>'
                  '<coordinates>-95.265,38.959,0</coordinates>'
                  '</Point>'
                  '</Placemark>'
              '</Document>'
            '</kml>'
            ).encode('ascii')
        )

    def test_basic_kml_document(self):
        """Tests the creation of a basic KML with Google Extensions ."""
        doc = KML.kml(
            GX.Tour(
                GX.Playlist(
                    GX.SoundCue(
                        KML.href("http://dev.keyhole.com/codesite/cntowerfacts.mp3")
                    ),
                    GX.Wait(
                        GX.duration(10)
                    ),
                    GX.FlyTo(
                        GX.duration(5),
                        GX.flyToMode("bounce"),
                        KML.LookAt(
                            KML.longitude(-79.387),
                            KML.latitude(43.643),
                            KML.altitude(0),
                            KML.heading(-172.3),
                            KML.tilt(10),
                            KML.range(1200),
                            KML.altitudeMode("relativeToGround"),
                        )
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<gx:Tour>'
                '<gx:Playlist>'
                  '<gx:SoundCue>'
                    '<href>http://dev.keyhole.com/codesite/cntowerfacts.mp3</href>'
                  '</gx:SoundCue>'
                  '<gx:Wait>'
                    '<gx:duration>10</gx:duration>'
                  '</gx:Wait>'
                  '<gx:FlyTo>'
                    '<gx:duration>5</gx:duration>'
                    '<gx:flyToMode>bounce</gx:flyToMode>'
                    '<LookAt>'
                      '<longitude>-79.387</longitude>'
                      '<latitude>43.643</latitude>'
                      '<altitude>0</altitude>'
                      '<heading>-172.3</heading>'
                      '<tilt>10</tilt>'
                      '<range>1200</range>'
                      '<altitudeMode>relativeToGround</altitudeMode>'
                    '</LookAt>'
                  '</gx:FlyTo>'
                '</gx:Playlist>'
              '</gx:Tour>'
            '</kml>'
            ).encode('ascii')
        )

    def test_kml_document_with_atom_element(self):
        """Tests the creation of a KML document with an ATOM element."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<atom:author>'
                  '<atom:name>J. K. Rowling</atom:name>'
                '</atom:author>'
                '<atom:link href="http://www.harrypotter.com"/>'
                '<Placemark>'
                  '<name>Hogwarts</name>'
                  '<Point>'
                    '<coordinates>1,1</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
            ).encode('ascii')
        )

    def test_kml_document_with_cdata_description(self):
        """Tests the creation of a KML document with a CDATA element."""
        doc = KML.description(
            '<h1>CDATA Tags are useful!</h1>'
        )
        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<description '
              'xmlns:gx="http://www.google.com/kml/ext/2.2" '
              'xmlns:atom="http://www.w3.org/2005/Atom" '
              'xmlns="http://www.opengis.net/kml/2.2">'
              '&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;'
            '</description>'
            ).encode('ascii')
        )

    def test_kml_document_with_cdata_description_2(self):
        """Tests the creation of a KML document with a CDATA element."""
        doc = KML.kml(
            KML.Document(
                KML.Placemark(
                    KML.name("CDATA example"),
                    KML.description(
                        '<h1>CDATA Tags are useful!</h1>'
                        '<p><font color="red">Text is <i>more readable</i> and '
                        '<b>easier to write</b> when you can avoid using entity '
                        'references.</font></p>'
                    ),
                    KML.Point(
                        KML.coordinates("102.595626,14.996729"),
                    ),
                ),
            ),
        )
        self.assertXmlEquivalentOutputs(
            etree.tostring(doc, encoding='ascii'), (
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>CDATA example</name>'
                  '<description>'
                    '&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;'
                    '&lt;p&gt;&lt;font color="red"&gt;Text is &lt;i&gt;more readable&lt;/i&gt; and '
                    '&lt;b&gt;easier to write&lt;/b&gt; when you can avoid using entity '
                    'references.&lt;/font&gt;&lt;/p&gt;'
                  '</description>'
                  '<Point>'
                    '<coordinates>102.595626,14.996729</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
            ).encode('ascii')
        )


class GeneratePythonScriptTestCase(unittest.TestCase, xmlunittest.XmlTestMixin):
    def test_write_python_script_for_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        script = write_python_script_for_kml_document(doc)
        self.assertEqual(
            script,
            'from __future__ import unicode_literals\n'
            'from __future__ import print_function\n'
            'from lxml import etree\n'
            'from pykml.factory import KML_ElementMaker as KML\n'
            'from pykml.factory import ATOM_ElementMaker as ATOM\n'
            'from pykml.factory import GX_ElementMaker as GX\n'
            '\n'
            'doc = KML.kml(\n'
            '  KML.Document(\n'
            '    ATOM.author(\n'
            '      ATOM.name(\'J. K. Rowling\'),\n'
            '    ),\n'
            '    ATOM.link(  href="http://www.harrypotter.com",\n'
            '),\n'
            '    KML.Placemark(\n'
            '      KML.name(\'Hogwarts\'),\n'
            '      KML.Point(\n'
            '        KML.coordinates(\'1,1\'),\n'
            '      ),\n'
            '    ),\n'
            '  ),\n'
            ')\n'
            'print(etree.tostring(etree.ElementTree(doc), \n'
            '      encoding=\'utf-8\', \n'
            '      xml_declaration=True, \n'
            '      pretty_print=True).decode(\'utf-8\'))\n'
        )

    def test_write_python_script_for_multiline_coordinate_string(self):
        """Tests the creation of a trivial OGC KML document."""
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_reference/altitudemode_reference.kml'
        )
        with open(test_datafile, 'rb') as f:
            doc = parse(f, schema=None)
        script = write_python_script_for_kml_document(doc)
        self.assertEqual(
            script, (
                'from __future__ import unicode_literals\n'
                'from __future__ import print_function\n'
                'from lxml import etree\n'
                'from pykml.factory import KML_ElementMaker as KML\n'
                'from pykml.factory import ATOM_ElementMaker as ATOM\n'
                'from pykml.factory import GX_ElementMaker as GX\n'
                '\n'
                'doc = KML.kml(\n'
                '  etree.Comment(\' required when using gx-prefixed elements \'),\n'
                '  KML.Placemark(\n'
                '    KML.name(\'gx:altitudeMode Example\'),\n'
                '    KML.LookAt(\n'
                '      KML.longitude(\'146.806\'),\n'
                '      KML.latitude(\'12.219\'),\n'
                '      KML.heading(\'-60\'),\n'
                '      KML.tilt(\'70\'),\n'
                '      KML.range(\'6300\'),\n'
                '      GX.altitudeMode(\'relativeToSeaFloor\'),\n'
                '    ),\n'
                '    KML.LineString(\n'
                '      KML.extrude(\'1\'),\n'
                '      GX.altitudeMode(\'relativeToSeaFloor\'),\n'
                '      KML.coordinates(\n'
                '      {0}\'146.825,12.233,400 \'\n'
                '      {0}\'146.820,12.222,400 \'\n'
                '      {0}\'146.812,12.212,400 \'\n'
                '      {0}\'146.796,12.209,400 \'\n'
                '      {0}\'146.788,12.205,400 \'\n'
                '      ),\n'
                '    ),\n'
                '  ),\n'
                ')\n'
                'print(etree.tostring(etree.ElementTree(doc), \n'
                '      encoding=\'utf-8\', \n'
                '      xml_declaration=True, \n'
                '      pretty_print=True).decode(\'utf-8\'))\n'
            ).format('' if six.PY3 else 'u')
        )

    def test_write_python_script_for_kml_document_with_cdata(self):
        """Tests the creation of an OGC KML document with a cdata tag"""
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_tutorial/using_the_cdata_element.kml'
        )
        schema = Schema('kml22gx.xsd')
        with open(test_datafile, 'rb') as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)
        self.assertEqual(
            script, (
                'from __future__ import unicode_literals\n'
                'from __future__ import print_function\n'
                'from lxml import etree\n'
                'from pykml.factory import KML_ElementMaker as KML\n'
                'from pykml.factory import ATOM_ElementMaker as ATOM\n'
                'from pykml.factory import GX_ElementMaker as GX\n'
                '\n'
                'doc = KML.kml(\n'
                '  KML.Document(\n'
                '    KML.Placemark(\n'
                '      KML.name(\'CDATA example\'),\n'
                '      KML.description(\n'
                '          {0}\'<h1>CDATA Tags are useful!</h1> \'\n'
                '          {0}\'<p><font color="red">Text is <i>more readable</i> and \'\n'
                '          {0}\'<b>easier to write</b> when you can avoid using entity \'\n'
                '          {0}\'references.</font></p> \'\n'
                '      ),\n'
                '      KML.Point(\n'
                '        KML.coordinates(\'102.595626,14.996729\'),\n'
                '      ),\n'
                '    ),\n'
                '  ),\n'
                ')\n'
                'print(etree.tostring(etree.ElementTree(doc), \n'
                '      encoding=\'utf-8\', \n'
                '      xml_declaration=True, \n'
                '      pretty_print=True).decode(\'utf-8\'))\n'
            ).format('' if six.PY3 else 'u')
        )
        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            tfile = f.name
            # print(tfile)
            f.write(script)

        # execute the temporary python file to create a KML file

        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(
            os.path.join(path.dirname(__file__), '../..')
        )
        if six.PY2:
            current_env['PYTHONPATH'] = str(current_env['PYTHONPATH'])

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            exit_code = subprocess.call(
                ["python", tfile],
                stdout=f,
                env=current_env
            )
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')

        os.unlink(tfile)
        os.unlink(temp_kml_file)

    def test_write_python_script_for_kml_document_with_namespaces(self):
        """Tests the creation of an OGC KML document with several namespaces"""
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        schema = Schema('kml22gx.xsd')
        with open(test_datafile, 'rb') as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)

        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            tfile = f.name
            # print(tfile)  # uncomment to print the temporary filename
            f.write(script)

        # execute the temporary python file to create a KML file
        # set the PYTHONPATH variable so that it references the root
        # of the pyKML library

        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(
            os.path.join(path.dirname(__file__), '../..')
        )
        if six.PY2:
            current_env['PYTHONPATH'] = str(current_env['PYTHONPATH'])

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            exit_code = subprocess.call(["python", tfile], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')

        os.unlink(tfile)
        os.unlink(temp_kml_file)

    def test_write_python_script_for_kml_document_with_comments(self):
        """Tests the creation of an OGC KML document with several comments"""
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'simple_file_with_comments.kml'
        )
        schema = Schema('kml22gx.xsd')
        with open(test_datafile, 'rb') as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)

        # create a temporary python file
        with tempfile.NamedTemporaryFile(mode='wt', suffix='.py', delete=False) as f:
            tfile = f.name
            # print(tfile)
            f.write(script)

        # execute the temporary python file to create a KML file

        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(
            os.path.join(path.dirname(__file__), '../..')
        )
        if six.PY2:
            current_env['PYTHONPATH'] = str(current_env['PYTHONPATH'])

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.kml', delete=False) as f:
            temp_kml_file = f.name
            # print(temp_kml_file)  # Useful for debugging
            exit_code = subprocess.call(["python", tfile], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)

        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')
        # test that the original and generated documents are equivalent
        self.assertXmlEquivalentOutputs(etree.tostring(doc), etree.tostring(doc2))

        os.unlink(tfile)
        os.unlink(temp_kml_file)


if __name__ == '__main__':
    unittest.main()
