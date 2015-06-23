#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
"""pyKML Helpers Module

The pykml.helpers module contains 'helper' functions that operate on pyKML 
document objects for accomplishing common tasks.

"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import re
from decimal import Decimal

from pykml.factory import KML_ElementMaker as KML


def separate_namespace(qname):
    """Separates the namespace from the element"""

    try:
        namespace, element_name = re.search('^{(.+)}(.+)$', qname).groups()
    except:
        namespace = None
        element_name = qname
    return namespace, element_name


def set_max_decimal_places(doc, max_decimals):
    """Sets the maximum number of decimal places used by KML elements.

    - Elements of a vertex are delimited by single commas.
    - Vertices are delimited by one or more space characters.

    This method facilitates reducing the file size of a KML document.
    """

    def replace_delimited_string_member(
            delimited_str,
            separator,
            index_no_,
            q):
        """Modify the number of decimal places for a delimited string member"""
        values = delimited_str.split(separator)
        values[index_no_] = str(Decimal(values[index_no_]).quantize(q))

        return separator.join(values)

    # Create Decimal quantization here for later lookup.
    q_lookup = {}
    for data_type, decimal_places in max_decimals.items():
        # 2 places --> '0.01'
        q_lookup[data_type] = Decimal(10) ** -decimal_places

    del max_decimals

    if 'longitude' in q_lookup:
        data_type = 'longitude'
        index_no = 0  # longitude is in the first position
        # modify <longitude> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}longitude'):
            new_val = Decimal(el.text).quantize(q_lookup[data_type])
            el.getparent().longitude = KML.longitude(new_val)
        # modify <coordinates> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
            vertex_str_list = []
            for vertex in el.text.strip().split(' '):
                vertex_str_list.append(
                    replace_delimited_string_member(
                        delimited_str=vertex,
                        separator=',',
                        index_no_=index_no,
                        q=q_lookup[data_type]
                    )
                )
            el_new = KML.coordinates(' '.join(vertex_str_list).strip())
            el.getparent().replace(el, el_new)
        # modify <gx:coords> elements
        for el in doc.findall('.//{http://www.google.com/kml/ext/2.2}coord'):
            el._setText(
                replace_delimited_string_member(
                    delimited_str=el.text,
                    separator=' ',
                    index_no_=index_no,
                    q=q_lookup[data_type]
                )
            )

    if 'latitude' in q_lookup:
        data_type = 'latitude'
        index_no = 1  # latitude is in the second position
        # modify <latitude> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}latitude'):
            new_val = Decimal(el.text).quantize(q_lookup[data_type])
            el.getparent().latitude = KML.latitude(new_val)
        # modify <coordinates> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
            vertex_str_list = []
            for vertex in el.text.strip().split(' '):
                vertex_str_list.append(
                    replace_delimited_string_member(
                        delimited_str=vertex,
                        separator=',',
                        index_no_=index_no,
                        q=q_lookup[data_type]
                    )
                )
            el_new = KML.coordinates(' '.join(vertex_str_list).strip())
            el.getparent().replace(el, el_new)
        # modify <gx:coords> elements
        for el in doc.findall('.//{http://www.google.com/kml/ext/2.2}coord'):
            el._setText(
                replace_delimited_string_member(
                    delimited_str=el.text,
                    separator=' ',
                    index_no_=index_no,
                    q=q_lookup[data_type]
                )
            )

    if 'altitude' in q_lookup:
        data_type = 'altitude'
        index_no = 2  # altitude is in the third position
        # modify <altitude> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}altitude'):
            new_val = Decimal(el.text).quantize(q_lookup[data_type])
            el.getparent().altitude = KML.altitude(new_val)
        # modify <coordinates> elements
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
            vertex_str_list = []
            for vertex in el.text.strip().split(' '):
                vertex_str_list.append(
                    replace_delimited_string_member(
                        delimited_str=vertex,
                        separator=',',
                        index_no_=index_no,
                        q=q_lookup[data_type]
                    )
                )
            el_new = KML.coordinates(' '.join(vertex_str_list).strip())
            el.getparent().replace(el, el_new)
        # modify <gx:coords> elements
        for el in doc.findall('.//{http://www.google.com/kml/ext/2.2}coord'):
            el._setText(
                replace_delimited_string_member(
                    delimited_str=el.text,
                    separator=' ',
                    index_no_=index_no,
                    q=q_lookup[data_type]
                )
            )

    if 'heading' in q_lookup:
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}heading'):
            new_val = Decimal(el.text).quantize(q_lookup['heading'])
            el.getparent().heading = KML.heading(new_val)
    if 'tilt' in q_lookup:
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}tilt'):
            new_val = Decimal(el.text).quantize(q_lookup['tilt'])
            el.getparent().tilt = KML.tilt(new_val)
    if 'range' in q_lookup:
        for el in doc.findall('.//{http://www.opengis.net/kml/2.2}range'):
            new_val = Decimal(el.text).quantize(q_lookup['range'])
            el.getparent().range = KML.range(new_val)
