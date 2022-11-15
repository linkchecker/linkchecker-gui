# Copyright (C) 2011-2014 Bastian Kleineidam
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

import os
import sys


def get_profile_dir():
    """Return path where all profiles of current user are stored."""
    return os.path.join(os.environ["HOME"], "Library", "Safari")


def find_bookmark_file():
    """Return the bookmark file of the Default profile.
    Returns absolute filename if found, or empty string if no bookmark file
    could be found.
    """
    if sys.platform != "darwin":
        return ""
    try:
        dirname = get_profile_dir()
        if os.path.isdir(dirname):
            fname = os.path.join(dirname, "Bookmarks.plist")
            if os.path.isfile(fname):
                return fname
    except Exception:
        pass
    return ""
