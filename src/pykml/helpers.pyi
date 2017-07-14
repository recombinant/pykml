#
# coding: utf-8
#
# Stub file for pyxml.helpers
#
from decimal import Decimal
from typing import Optional, Tuple, Dict, Any

from lxml import etree


def separate_namespace(qname: str) \
        -> Tuple[Optional[str], str]:
    ...


def _replace_delimited_string_member(delimited_str: str,
                                     separator: str,
                                     index_no_: int,
                                     q: Decimal) \
        -> str:
    ...


# TODO: max_decimals
def set_max_decimal_places(doc: etree.XMLParser,
                           max_decimals: Dict[Any, int]) \
        -> None:
    ...
