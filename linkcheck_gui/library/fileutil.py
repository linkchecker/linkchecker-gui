# Copyright (C) 2005-2014 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
File and path utilities.
"""

import os
from functools import lru_cache


@lru_cache(128)
def is_writable(filename):
    """Check if
    - the file is a regular file and is writable, or
    - the file does not exist and its parent directory exists and is
      writable
    """
    if not os.path.exists(filename):
        parentdir = os.path.dirname(filename)
        return os.path.isdir(parentdir) and os.access(parentdir, os.W_OK)
    return os.path.isfile(filename) and os.access(filename, os.W_OK)
