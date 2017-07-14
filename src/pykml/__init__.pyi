#
# coding: utf-8
#
# Stub file for pykml.__init__
#
from typing import NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    macro: int
    releaselevel: str
    serial: int


version_info: VersionInfo = ...

version: str = ...
