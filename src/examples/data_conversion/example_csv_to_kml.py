#!/usr/bin/env python
# -*- mode: python tab-width: 4 coding: utf-8 -*-
"""Example of generating KML from data in a CSV file

References:

http://earthquake.usgs.gov/earthquakes/feed/
http://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import csv
from datetime import datetime
from lxml import etree
import six
from six.moves.urllib.request import urlopen
from pykml.factory import KML_ElementMaker as KML
from pykml.parser import Schema
from pykml.util import format_xml_with_cdata


def make_extended_data_elements(datadict):
    """Converts a dictionary to ExtendedData/Data elements"""
    edata = KML.ExtendedData()
    for key, value in datadict.items():
        edata.append(KML.Data(KML.value(value), name=key + '_'))
    return edata


def get_balloon_style():
    """
    A separate instance of KML.BalloonStyle() needs to be created for each
    KML.Style(). The KML.text() will be formatted as CDATA
    """
    return KML.BalloonStyle(
        KML.text("""
        <table Border=1>
          <tr><th>Earthquake ID</th><td>$[id_]</td></tr>
          <tr><th>Magnitude</th><td>$[mag_]</td></tr>
          <tr><th>Depth</th><td>$[depth_]</td></tr>
          <tr><th>Datetime</th><td>$[time_]</td></tr>
          <tr><th>Coordinates</th><td>($[longitude_],$[latitude_])</td></tr>
          <tr><th>Region</th><td>$[place_]</td></tr>
        </table>"""),
    )


def main():
    """
    Create a KML document with a folder and a style for each earthquake
    magnitude
    """
    doc = KML.Document()

    icon_styles = [
        [2, 'ff000000'],
        [3, 'ffff0000'],
        [4, 'ff00ff55'],
        [5, 'ffff00aa'],
        [6, 'ff00ffff'],
        [7, 'ff0000ff'],
    ]

    # create a series of Icon Styles
    for threshold, color in icon_styles:
        doc.append(
            KML.Style(
                KML.IconStyle(
                    KML.color(color),
                    KML.scale(threshold / 2),
                    KML.Icon(
                        KML.href('http://maps.google.com/mapfiles/kml/shapes/earthquake.png'),
                    ),
                    KML.hotSpot(x='0.5', y='0', xunits='fraction', yunits='fraction'),
                ),
                get_balloon_style(),
                id='earthquake-style-{threshold}'.format(threshold=threshold),
            )
        )

    doc.append(KML.Folder())

    # read in a csv file, and create a placemark for each record
    url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.csv'
    fileobject = urlopen(url)

    if six.PY3:  # fileobject is bytes, csv requires string
        import codecs
        fileobject = codecs.getreader('utf-8')(fileobject)

    for row in csv.DictReader(fileobject):
        timestamp = datetime.strptime(row['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        pm = KML.Placemark(
            KML.name('Magnitude={0}'.format(row['mag'])),
            KML.TimeStamp(
                KML.when(timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')),
            ),
            KML.styleUrl(
                '#earthquake-style-{thresh}'.format(
                    thresh=int(float(row['mag']))
                )
            ),
            make_extended_data_elements(row),
            KML.Point(
                KML.coordinates('{0},{1}'.format(row['longitude'], row['latitude']))
            )
        )
        doc.Folder.append(pm)

    # check if the schema is valid
    schema_gx = Schema('kml22gx.xsd')
    schema_gx.assertValid(doc)

    kml = KML.kml(doc)

    print(etree.tostring(format_xml_with_cdata(kml),
                         pretty_print=True,
                         encoding='utf-8',
                         xml_declaration=True).decode())


if __name__ == '__main__':
    main()
