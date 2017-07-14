#
# coding: utf-8
#
# Stub file for pyxml.factory
#
from typing import Optional, Dict

from lxml import objectify, etree

nsmap: Dict[Optional[str], str] = ...

KML_ElementMaker: objectify.ElementMaker = ...

ATOM_ElementMaker: objectify.ElementMaker = ...

GX_ElementMaker: objectify.ElementMaker = ...


def get_factory_object_name(namespace: Optional[str]) -> Optional[str]:
    ...


def write_python_script_for_kml_document(doc: etree.XMLParser) \
        -> str:
    ...


def kml2pykml():
    ...
