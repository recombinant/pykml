#
# coding: utf-8
#
# pykml.__init__
#
from collections import namedtuple

version_info = namedtuple('VersionInfo',
                          'major '
                          'minor '
                          'macro '
                          'releaselevel '
                          'serial')(0, 2, 1, 'alpha', 0)

version = '{}.{}.{}'.format(*version_info[:3])
