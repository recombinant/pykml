#
# coding: utf-8
#
#  Stub file for pyxml.parser
#
from typing import Dict, Optional

from lxml import etree

OGCKML_SCHEMA: str = ...


class Schema:
    schema: etree.XMLSchema = ...

    def __init__(self, schema: str) -> None:
        ...

    def validate(self, doc: etree.XMLParser) -> bool:
        ...

    def assertValid(self, doc: etree.XMLParser) -> bool:
        ...


# TODO: parse_func
def _parse_internal(source: bytes,
                    parse_func,
                    schema: Optional[Schema] = ...,
                    parser_options: Optional[Dict[str, str]] = ...) \
        -> etree.XMLParser:
    ...


def fromstring(text: bytes,
               schema: Optional[Schema] = ...,
               parser_options: Optional[Schema] = ...) \
        -> etree.XMLParser:
    ...


# TODO: fileobject
def parse(fileobject,
          schema: Optional[Schema] = ...,
          parser_options=Optional[Dict[str, str]]) \
        -> etree.XMLParser:
    ...


def validate_kml():
    ...
