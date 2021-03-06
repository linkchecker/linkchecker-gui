# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2016 Bastian Kleineidam
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
import unittest
import sys
from tests import need_pyqt, need_x11


class TestGui (unittest.TestCase):
    """Test OMT GUI client."""

    @need_pyqt
    @need_x11
    def test_gui (self):
        from PyQt4 import QtCore, QtGui, QtTest
        from linkcheck_gui import LinkCheckerMain
        app = QtGui.QApplication(sys.argv)
        window = LinkCheckerMain()
        window.show()
        QtTest.QTest.mouseClick(window.controlButton, QtCore.Qt.LeftButton)
        window.close()
        del window
        del app
