#!/usr/bin/python
# -*- mode: python tab-width: 4 coding: utf-8 -*-
#
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
# from __future__ import unicode_literals
import sys
import getopt
from pykml.parser import parse
from pykml.parser import Schema
from pykml.factory import write_python_script_for_kml_document


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        # main code
        schema = Schema("kml22gx.xsd")
        filename = argv[1]
        with open(filename) as f:
            kmldoc = parse(f, schema=schema)
            print(write_python_script_for_kml_document(kmldoc))

    except Usage, err:
        print(err.msg, file=sys.stderr)
        print('for help use --help', file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
