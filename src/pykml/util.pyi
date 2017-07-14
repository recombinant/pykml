#
# coding: utf-8
#
# Stub file for pyxml.util
#
from contextlib import contextmanager
from typing import Sequence, List, Any, Optional, Dict, TypeVar, Iterable

from lxml import etree

from pykml.factory import KML_ElementMaker as KML


def clean_xml_string(input_string: str) -> str:
    ...


def format_xml_with_cdata(obj: etree._Element,
                          cdata_elements: Iterable[str] = ...) \
        -> etree._Element:
    ...


def count_elements(doc: etree.XMLParser) \
        -> Dict[Optional[str], Dict[str, int]]:
    ...


Angle = TypeVar['Angle', Sequence[int], int]


def wrap_angle180(angle: Angle) -> Angle:
    ...


def to_wkt_list(doc: etree.XMLParser) \
        -> List[str]:
    ...


@contextmanager
def open_pykml_uri(uri: str, mode: str = ...) -> None:
    ...


# TODO: fileobject
def convert_csv_to_kml(
        fileobject: Any,
        latitude_field: str = ...,
        longitude_field: str = ...,
        altitude_field: str = ...,
        name_field: str = ...,
        description_field: str = ...,
        snippet_field: str = ...,
) -> KML.kml:
    ...


def csv2kml() -> None:
    ...
