#
# -*- mode: python tab-width: 4 coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple

version_info = namedtuple('VersionInfo',
                          'major '
                          'minor '
                          'macro '
                          'releaselevel '
                          'serial')(0, 2, 1, 'alpha', 0)

version = '{}.{}.{}'.format(*version_info[:3])
