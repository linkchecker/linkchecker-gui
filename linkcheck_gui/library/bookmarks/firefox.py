# Copyright (C) 2010-2014 Bastian Kleineidam
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
import glob


def get_profile_dir():
    """Return path where all profiles of current user are stored."""
    if os.name == "nt":
        basedir = os.environ["APPDATA"]
        dirpath = os.path.join(basedir, "Mozilla", "Firefox", "Profiles")
    elif os.name == "posix":
        dirpath = os.path.join(os.environ["HOME"], ".mozilla", "firefox")
    return dirpath


def find_bookmark_file(profile="*.default-[0-9]*"):
    """Return the first found places.sqlite file of the profile directories
    ending with '.default' (or another given profile name).
    Returns absolute filename if found, or empty string if no bookmark file
    could be found.
    """
    try:
        for dirname in glob.glob(os.path.join(get_profile_dir(), profile)):
            if os.path.isdir(dirname):
                fname = os.path.join(dirname, "places.sqlite")
                if os.path.isfile(fname):
                    return fname
    except Exception:
        pass
    return ""
