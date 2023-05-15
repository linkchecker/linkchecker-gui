# Copyright (C) 2023 Chris Mayo
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
import tempfile
import unittest

from linkcheck_gui.library import fileutil


class TestFileUtil(unittest.TestCase):
    """Test fileutil module."""

    def test_fileutil(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.close()
        assert fileutil.is_writable(fp.name)
        os.remove(fp.name)
