#!/usr/bin/python
# -*- mode: python tab-width: 4 coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
# from __future__ import unicode_literals
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from math import cos, sin, radians

kmlobj = KML.kml(
    KML.Document()
)
for i in range(0, 360 * 2, 10):
    kmlobj.Document.append(
        KML.Placemark(
            KML.name('Hello World!'),
            KML.Point(
                KML.extrude(1),
                KML.altitudeMode('relativeToGround'),
                KML.coordinates('{lon},{lat},{alt}'.format(
                    lon=-91.35 + i / 100.0 * cos(radians(i)),
                    lat=0.0 + i / 100.0 * sin(radians(i)),
                    alt=i * 1000,
                ),
                ),
            ),
        )
    )

print(etree.tostring(etree.ElementTree(kmlobj), pretty_print=True))
