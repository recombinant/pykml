#!/usr/bin/python
#
# coding: utf-8
#
# utilities/kml2pykml.py
#
import argparse
import os
from contextlib import contextmanager
from os import sys

import requests

from pykml import version as pykml_version
from pykml.factory import write_python_script_for_kml_document
from pykml.parser import parse


class FileOpenException(Exception):
    pass


@contextmanager
def get_xml_file_object(uri):
    if os.path.isfile(uri):
        # XML is a binary stream (encoded text)
        file_object = open(uri, 'rb')
        yield file_object
        file_object.close()
        return

    try:
        r = requests.get(uri, stream=True)
        if r.status_code == requests.codes.ok:
            yield r.raw
            r.close()
        else:
            raise FileOpenException('GET status code {}'.format(r.status_code))

    except requests.exceptions.ConnectionError:
        raise FileOpenException('No internet connection?')

    except requests.exceptions.InvalidSchema:
        raise FileOpenException('Non-existent file or url')


def kml2pykml(*args):
    if args is None:
        args = sys.argv

    parser = argparse.ArgumentParser(description='Convert KML to pyKML')
    parser.add_argument('input', help='file name or URL of KML')
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {pykml_version}')

    # ArgumentParser can throw a SystemExit
    namespace = parser.parse_args(args=args)

    try:
        with get_xml_file_object(namespace.input) as file_object:
            # There is no schema as no validation occurs
            kmldoc = parse(file_object)
            print(write_python_script_for_kml_document(kmldoc))
            return 0

    except FileOpenException as e:
        print('Unable to retrieve "{}"'.format(namespace.input), file=sys.stderr)
        print('Error:', e.args[0], file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(kml2pykml('https://developers.google.com/kml/documentation/KML_Samples.kml'))
