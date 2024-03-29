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

from . import configuration
from PyQt6 import QtCore, QtWidgets, QtHelp


class HelpWindow(QtWidgets.QDialog):
    """A custom help display dialog."""

    def __init__(self, parent, qhcpath):
        """Initialize dialog and load qhc help project from given path."""
        super().__init__(parent)
        self.engine = QtHelp.QHelpEngine(qhcpath, self)
        self.engine.setupData()
        self.setWindowTitle("%s Help" % configuration.AppName)
        self.build_ui()

    def build_ui(self):
        """Build UI for the help window."""
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.browser = HelpBrowser(splitter, self.engine)
        self.tree = self.engine.contentWidget()
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.linkActivated.connect(self.browser.setSource)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.browser)
        splitter.setSizes((70, 530))
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(splitter)
        self.setLayout(hlayout)
        self.resize(800, 600)

    def showDocumentation(self, url):
        """Show given URL in help browser."""
        self.tree.expandAll()
        self.browser.setSource(url)
        self.show()


class HelpBrowser(QtWidgets.QTextBrowser):
    """A QTextBrowser that can handle qthelp:// URLs."""

    def __init__(self, parent, engine):
        """Initialize and store given HelpEngine instance."""
        super().__init__(parent)
        self.engine = engine

    def setSource(self, url):
        """Open HTTPS URLs in external browser, else call base class
        implementation."""
        if url.scheme() == "https":
            import webbrowser

            webbrowser.open(str(url.toString()))
        else:
            QtWidgets.QTextBrowser.setSource(self, url)

    def loadResource(self, rtype, url):
        """Handle qthelp:// URLs, load content from help engine."""
        if url.scheme() == "qthelp":
            return QtCore.QVariant(self.engine.fileData(url))
        return QtWidgets.QTextBrowser.loadResource(self, rtype, url)
