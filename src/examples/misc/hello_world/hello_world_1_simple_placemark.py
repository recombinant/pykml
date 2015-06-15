#!/usr/bin/python
# -*- mode: python tab-width: 4 coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

doc = KML.kml(
    KML.Placemark(
        KML.name('Hello World!'),
        KML.Point(
            KML.coordinates('-91.35,0,0'),
        ),
    ),
)
print(etree.tostring(etree.ElementTree(doc),
                     encoding='utf-8',
                     xml_declaration=True,
                     pretty_print=True).decode())
