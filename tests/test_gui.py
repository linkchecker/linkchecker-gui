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
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import pytest

try:
    from PyQt6 import QtCore, QtGui, QtTest, QtWidgets
except ImportError:
    pass

from linkcheck import configuration as linkchecker_configuration

from . import has_pyqt, has_x11


@pytest.mark.skipif(not has_pyqt, reason="PyQt required")
@pytest.mark.skipif(not has_x11, reason="X Display required")
class TestGui(unittest.TestCase):
    """ Test LinkChecker-GUI """
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.home_dir = tempfile.mkdtemp()
        os.environ["HOME"] = self.home_dir

    def tearDown(self):
        del self.app
        shutil.rmtree(self.home_dir)

    def test_start(self):
        """ Start checking button """
        from linkcheck_gui import LinkCheckerMain

        window = LinkCheckerMain()
        window.checker.finished.connect(window.close)
        window.options.ignorelines.setPlainText("ignore")
        window.options.warninglines.setPlainText("warning")
        window.urlinput.setText("http://localhost/linkcheck-gui")
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        QtTest.QTest.mouseClick(window.controlButton, QtCore.Qt.MouseButton.LeftButton)
        self.app.exec()
        del window

    @patch("PyQt6.QtWidgets.QFileDialog.getOpenFileName")
    @patch("PyQt6.QtWidgets.QFileDialog.getSaveFileName")
    def test_project(self, mock_get_save_filename, mock_get_open_filename):
        """ File/{Save,Open} project """
        from linkcheck_gui import LinkCheckerMain, projects

        project_file = os.path.join(self.home_dir, "project.lcp")
        mock_get_save_filename.side_effect = \
            lambda parent, title, suggestedname, ProjectFilter: (project_file, "lcp")
        mock_get_open_filename.side_effect = \
            lambda parent, title, suggestedname, ProjectFilter: (project_file, "lcp")
        window = LinkCheckerMain()
        window.urlinput.setText("http://localhost/linkcheck-gui")
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        projects.saveproject(window, "http://localhost/linkcheck-gui")
        projects.openproject(window)
        del window

    @patch("linkcheck.log.warn")
    def test_view_source(self, mock_log_warn):
        """ View Source """
        from linkcheck_gui import LinkCheckerMain

        mock_log_warn.side_effect = lambda level, message: None
        window = LinkCheckerMain()
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        window.view_source("http://localhost/linkcheck-gui", 1, 1)
        QtTest.QTest.qWaitForWindowExposed(window.editor)
        window.editor.editor.setModified(False)
        window.editor.close()
        del window

    def test_help(self):
        """ View Help """
        from linkcheck_gui import LinkCheckerMain

        window = LinkCheckerMain()
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        window.actionHelp.activate(QtGui.QAction.ActionEvent.Trigger)
        QtTest.QTest.qWaitForWindowExposed(window.assistant)
        del window

    def test_options(self):
        """ Edit/Options """
        from linkcheck_gui import options

        window = options.LinkCheckerOptions()
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        # Edit button
        QtTest.QTest.mouseClick(
            window.user_config_button, QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWaitForWindowExposed(window.editor)
        QtTest.QTest.mouseClick(window.closeButton, QtCore.Qt.MouseButton.LeftButton)
        del window

    @patch("PyQt6.QtWidgets.QFileDialog.getSaveFileName")
    def test_editor(self, mock_get_save_filename):
        """ Editor """
        from linkcheck_gui import editor

        editor_file = os.path.join(self.home_dir, "test_editor.file")
        mock_get_save_filename.side_effect = \
            lambda _dummy, title, basedir: (editor_file, None)
        window = editor.EditorWindow(None)
        window.setUrl("file:///test")
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        window.setText("test editor")
        window.actionSave.activate(QtGui.QAction.ActionEvent.Trigger)
        del window

    def test_qt_editor(self):
        """ Qt editor """
        from linkcheck_gui import editor_qt

        window = editor_qt.Editor(None)
        window.show()
        QtTest.QTest.qWaitForWindowExposed(window)
        del window

    def test_configuration(self):
        """ Modules Info """
        from linkcheck_gui import configuration

        assert "6." in configuration.get_modules_info()

    def test_highlighter(self):
        """ Highlighter """
        from linkcheck_gui import syntax

        testDoc = QtGui.QTextDocument()
        testDoc.setPlainText("test")
        x = syntax.XmlHighlighter(testDoc)
        x.highlightBlock("test")
        syntax.IniHighlighter(testDoc)

    def test_validator(self):
        """ PyRegexValidator """
        from linkcheck_gui import validator

        v = validator.PyRegexValidator()
        state, pos = v.validate(r"\d", 0)
        assert state == QtGui.QValidator.State.Acceptable

    @patch("PyQt6.QtWidgets.QFileDialog.getSaveFileName")
    def test_urlsave(self, mock_get_save_filename):
        """ urlsave """
        from linkcheck_gui import urlmodel, urlsave

        class MockParent:
            saveresultas = None

        save_file = os.path.join(self.home_dir, "test_urlsave.html")
        mock_get_save_filename.side_effect = \
            lambda parent, title, filename, filters: (save_file, "HTML output (*.html)")
        config = linkchecker_configuration.Configuration()
        config["logger"] = config.logger_new("none")
        m = urlmodel.UrlItemModel()
        urlsave(MockParent(), config, m.urls)
