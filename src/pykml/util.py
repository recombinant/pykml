#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
""" pyKML Utility Module

The pykml.utility module provides utility functions that operate on KML
documents
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import re
from contextlib import contextmanager
import ssl
from optparse import OptionParser
import csv

from lxml import etree

from pykml.factory import KML_ElementMaker as KML
from pykml import version as pykml_version
from six.moves.urllib.request import urlopen


def clean_xml_string(input_string):
    """removes invalid characters from an XML string"""
    return input_string.encode('ascii', 'ignore').decode('ascii')


def format_xml_with_cdata(
        obj,
        cdata_elements=('description',
                        'text',
                        'linkDescription',
                        'displayName', )):
    # Convert Objectify document to lxml.etree (is there a better way?)
    root = etree.fromstring(etree.tostring(etree.ElementTree(obj)))

    # Create an xpath expression to search for all desired cdata elements
    xpath = '|'.join('//kml:' + tag for tag in cdata_elements)

    results = root.xpath(
        xpath,
        namespaces={'kml': 'http://www.opengis.net/kml/2.2'}
    )
    for element in results:
        element.text = etree.CDATA(element.text)
    return root


def count_elements(doc):
    """Counts the number of times each element is used in a document"""
    summary = {}
    for el in doc.iter():
        try:
            namespace, element_name = re.search('^{(.+)}(.+)$', el.tag).groups()
        except:
            namespace = None
            element_name = el.tag
        if namespace not in summary:
            summary[namespace] = {}
        if element_name not in summary[namespace]:
            summary[namespace][element_name] = 1
        else:
            summary[namespace][element_name] += 1
    return summary


def wrap_angle180(angle):
    # returns an angle such that -180 < angle <= 180
    try:
        # if angle is a sequence
        return [((a+180) % 360) - 180 for a in angle]
    except TypeError:
        return ((angle+180) % 360) - 180


def to_wkt_list(doc):
    """converts all geometries to Well Known Text format"""
    def ring_coords_to_wkt(ring):
        """converts LinearRing coordinates to WKT style coordinates"""
        return ((ring.coordinates.text.strip())
                .replace(' ', '@@')
                .replace(',', ' ')
                .replace('@@', ', '))

    ring_wkt_list = []
    context = etree.iterwalk(doc, events=("start",))
    for action, elem in context:
        if elem.tag in ['{http://www.opengis.net/kml/2.2}Polygon',
                        '{http://www.opengis.net/kml/2.2}MultiPolygon']:
            # print("%s: %s" % (action, elem.tag))
            if elem.tag == '{http://www.opengis.net/kml/2.2}Polygon':

                # outer boundary
                ringlist = [
                    '({0})'.format(
                        ring_coords_to_wkt(elem.outerBoundaryIs.LinearRing)
                    )
                ]
                for obj in elem.findall('{http://www.opengis.net/kml/2.2}innerBoundaryIs'):
                    ringlist.append(
                        '({0})'.format(
                            ring_coords_to_wkt(obj.LinearRing)
                        )
                    )

                wkt = 'POLYGON ({rings})'.format(rings=', '.join(ringlist))
                ring_wkt_list.append(wkt)
    return ring_wkt_list


@contextmanager
def open_pykml_uri(uri, mode='rt'):
    """
    Contextmanager to open a local or remote file and close when complete.

    :param uri: path to local file or url to remote file
    :return: handle to opened file
    """
    try:
        f = open(uri, mode)
    except IOError:
        context = ssl._create_unverified_context()
        f = urlopen(uri, context=context)

    yield f

    f.close()


def convert_csv_to_kml(
        fileobject,
        latitude_field='latitude',
        longitude_field='longitude',
        altitude_field='altitude',
        name_field='name',
        description_field='description',
        snippet_field='snippet',
):
    """Reads a CSV document from a file-like object and converts it to KML"""

    # create a basic KML document
    kmldoc = KML.kml(KML.Document(
        KML.Folder(
            KML.name("KmlFile"))
        )
    )

    csvdoc = csv.DictReader(fileobject)

    # if field is not found, check for other common field names
    if latitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['latitude', 'lat']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            latitude_field = match_field
    if longitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['longitude', 'lon', 'long']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            longitude_field = match_field
    if altitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['altitude', 'alt']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            altitude_field = match_field
    if name_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['name']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            name_field = match_field
    if snippet_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['snippet']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            snippet_field = match_field
    if description_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['description', 'desc']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            description_field = match_field

    # check that latitude and longitude columns can be found
    if latitude_field not in csvdoc.fieldnames:
        raise KeyError(
            'Latitude field ({0}) was not found in the CSV file '
            'column names {1}'.format(latitude_field, csvdoc.fieldnames)
        )
    if longitude_field not in csvdoc.fieldnames:
        raise KeyError(
            'Longitude field ({0}) was not found in the CSV file '
            'column names {1}'.format(longitude_field, csvdoc.fieldnames)
        )
    for row in csvdoc:
        pm = KML.Placemark()
        if name_field in row:
            pm.append(
                KML.name(clean_xml_string(row[name_field]))
            )
        if snippet_field in row:
            pm.append(
                KML.Snippet(clean_xml_string(row[snippet_field]), maxLines="2")
            )
        if description_field in row:
            pm.append(
                KML.description(clean_xml_string(row[description_field]))
            )
        else:
            desc = '<table border="1"'
            fmt = '<tr><th>{0}</th><td>{1}</td></tr>'
            # iterate through the cells in 'row' filling table
            for field_name in csvdoc.fieldnames:
                desc += fmt.format(field_name, row[field_name])
            desc += '</table>'
            pm.append(KML.description(clean_xml_string(desc)))

        coord_list = [row[longitude_field], row[latitude_field]]
        if altitude_field in row:
            coord_list += [row[altitude_field]]
        pm.append(
            KML.Point(
                KML.coordinates(','.join(coord_list))
            )
        )
        kmldoc.Document.Folder.append(pm)
    return kmldoc


def csv2kml():
    """Parse a CSV file and generates a KML document

    Example: csv2kml test.csv
    """
    parser = OptionParser(
        usage='usage: %prog FILENAME_or_URL',
        version='%prog {}'.format(pykml_version),
    )
    parser.add_option("--longitude_field", dest="longitude_field",
                      help="name of the column that contains longitude data")
    parser.add_option("--latitude_field", dest="latitude_field",
                      help="name of the column that contains latitude data")
    parser.add_option("--altitude_field", dest="altitude_field",
                      help="name of the column that contains altitude data")
    parser.add_option("--name_field", dest="name_field",
                      help="name of the column used for the placemark name")
    parser.add_option("--description_field", dest="description_field",
                      help="name of the column used for the placemark description")
    parser.add_option("--snippet_field", dest="snippet_field",
                      help="name of the column used for the placemark snippet text")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of arguments")
    else:
        uri = args[0]

    # try to open the URI as both a local file and a remote URL
    with open_pykml_uri(uri) as f:
        kmldoc = convert_csv_to_kml(
            f,
            latitude_field=options.latitude_field,
            longitude_field=options.longitude_field,
            altitude_field=options.altitude_field,
            name_field=options.name_field,
            description_field=options.description_field,
            snippet_field=options.snippet_field,
        )

    root = format_xml_with_cdata(kmldoc)

    print(etree.tostring(root,
                         encoding='ascii',
                         pretty_print=True,
                         xml_declaration=True).decode('ascii'))
