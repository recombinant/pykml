#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
"""pyKML Factory Module

The pykml.factory module provides objects and functions that can be used to 
create KML documents element-by-element. 
The factory module leverages `lxml's ElementMaker factory`_ objects to create
KML objects with the appropriate namespace prefixes.

.. _lxml: http://lxml.de
.. _lxml's ElementMaker factory: http://lxml.de/objectify.html#tree-generation-with-the-e-factory
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os
from os import sys
from collections import OrderedDict
from optparse import OptionParser

from lxml import etree, objectify
from six import StringIO, BytesIO

from pykml.parser import parse
from pykml import version as pykml_version

nsmap = OrderedDict([
    (None, 'http://www.opengis.net/kml/2.2'),
    ('atom', 'http://www.w3.org/2005/Atom'),
    ('gx', 'http://www.google.com/kml/ext/2.2'),
])

# create a factory object for creating objects in the KML namespace
KML_ElementMaker = objectify.ElementMaker(
    annotate=False,
    namespace=nsmap[None],
    nsmap=nsmap,
)
# create a factory object for creating objects in the ATOM namespace
ATOM_ElementMaker = objectify.ElementMaker(
    annotate=False,
    namespace=nsmap['atom'],
    nsmap={'atom': nsmap['atom']},
)
# Create a factory object for the KML Google Extension namespace
GX_ElementMaker = objectify.ElementMaker(
    annotate=False,
    namespace=nsmap['gx'],
    nsmap={'gx': nsmap['gx']},
)


def get_factory_object_name(namespace):
    """Returns the correct factory object for a given namespace"""

    factory_map = {
        'http://www.opengis.net/kml/2.2': 'KML',
        'http://www.w3.org/2005/Atom': 'ATOM',
        'http://www.google.com/kml/ext/2.2': 'GX'
    }
    if namespace:
        if namespace in factory_map:
            factory_object_name = factory_map[namespace]
        else:
            factory_object_name = None
    else:
        # use the KML factory object as the default, if no namespace is given
        factory_object_name = 'KML'
    return factory_object_name


def write_python_script_for_kml_document(doc):
    """Generates a python script that will construct a given KML document"""
    from pykml.helpers import separate_namespace

    output = StringIO()
    indent_size = 2

    # use unicode literals and print function as these are compatible
    # with PY2 & PY3
    output.write('from __future__ import unicode_literals\n')
    output.write('from __future__ import print_function\n')

    # add the etree package so that comments can be handled
    output.write('from lxml import etree\n')

    # add the namespace declaration section
    output.write('from pykml.factory import KML_ElementMaker as KML\n')
    output.write('from pykml.factory import ATOM_ElementMaker as ATOM\n')
    output.write('from pykml.factory import GX_ElementMaker as GX\n')
    output.write('\n')

    level = 0
    xml = BytesIO(etree.tostring(doc, encoding='utf-8', xml_declaration=True))
    context = etree.iterparse(xml, events=("start", "end", "comment"))
    output.write('doc = ')
    last_action = None
    main_element_processed_flag = False
    previous_list = []  # list of comments before the root element
    posterior_list = []  # list of comments after the root element
    for action, elem in context:
        # TODO: remove the following redundant conditional
        if action in ('start', 'end', 'comment'):
            namespace, element_name = separate_namespace(elem.tag)
            if action in ('comment', ):
                indent = ' ' * level * indent_size
                if elem.text:
                    text_list = elem.text.split('\n')
                    if len(text_list) == 1:
                        text = repr(elem.text)
                    else:  # len(text_list) > 1
                        # format and join all non-empty lines
                        text = '\n' + ''.join(
                            ['{indent}{content}\n'.format(
                                indent=' ' * (len(t) - len(t.lstrip())),
                                content=repr(t.strip() + ' '))
                             for t in text_list if len(t.strip()) > 0]
                        ) + indent
                else:
                    text = ''
                if level == 0:
                    # store the comment so that it can be appended later
                    if main_element_processed_flag:
                        posterior_list.append("{indent}etree.Comment({comment})".format(
                            indent=indent,
                            comment=text,
                        ))
                    else:
                        previous_list.append("{indent}etree.Comment({comment})".format(
                            indent=indent,
                            comment=text,
                        ))
                else:
                    output.write("{indent}etree.Comment({comment}),\n".format(
                        indent=indent,
                        comment=text,
                    ))
            elif action in ('start', ):
                main_element_processed_flag = True
                if last_action is None:
                    indent = ''
                else:
                    indent = ' ' * level * indent_size
                level += 1
                if elem.text:
                    # METHOD 1
                    # # treat all text string the same. this works but gets
                    # # messy for multi-line test strings
                    # text = repr(elem.text)
                    # METHOD 2 - format multiline strings differently
                    text_list = elem.text.split('\n')
                    if len(text_list) == 1:
                        text = repr(elem.text)
                    else:  # len(text_list) > 1
                        # format and join all non-empty lines
                        text = '\n' + ''.join(
                            ['{indent}{content}\n'.format(
                                indent=' ' * (len(t) - len(t.lstrip())),
                                content=repr(t.strip() + ' ')
                            ) for t in text_list if len(t.strip()) > 0]
                        ) + indent
                else:
                    text = ''
                output.write('{indent}{factory}.{tag}({text}\n'.format(
                    indent=indent,
                    factory=get_factory_object_name(namespace),
                    tag=element_name,
                    text=text,
                ))
            elif action in ('end', ):
                level -= 1
                if last_action == 'start':
                    output.seek(output.tell() - 1, os.SEEK_SET)  # TODO: ?
                    indent = ''
                else:
                    indent = ' ' * level * indent_size
                # NOTE: iteration order is implementation dependent
                # etree does not guarantee to preserve attribute list order
                for att, val in elem.items():
                    output.write('{0}  {1}="{2}",\n'.format(indent, att, val))
                output.write('{0}),\n'.format(indent))
        last_action = action

    # remove the last comma
    output.seek(output.tell() - 2, os.SEEK_SET)  # TODO: is this correct ?
    output.truncate()
    output.write('\n')

    for entry in previous_list:
        output.write('doc.addprevious({entry})\n'.format(
            entry=entry
        ))
    for entry in posterior_list:
        output.write('doc.addnext({entry})\n'.format(
            entry=entry
        ))

    # add python code to print out the KML document
    output.write('print(etree.tostring(etree.ElementTree(doc), \n'
                 '                     encoding=\'utf-8\', \n'
                 '                     xml_declaration=True, \n'
                 '                     pretty_print=True).decode(\'utf-8\'))\n')

    contents = output.getvalue()
    output.close()
    return contents


def kml2pykml():
    """Parses a KML file and generates a pyKML script"""
    from pykml.util import open_pykml_uri

    parser = OptionParser(
        usage='usage: %prog FILENAME_or_URL',
        version='%prog {}'.format(pykml_version),
    )
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of arguments")
    else:
        uri = args[0]

    with open_pykml_uri(uri, mode='rb') as f:
        doc = parse(f, schema=None)

    sys.stdout.write(write_python_script_for_kml_document(doc))
