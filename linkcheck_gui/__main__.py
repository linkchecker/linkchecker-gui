# Copyright (C) 2008-2016 Bastian Kleineidam
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
Check HTML pages for broken links. This is the GUI client.
"""
import signal
import sys

from linkcheck import configuration
from linkcheck.command.linkchecker import drop_privileges
from linkcheck.fileutil import is_readable
from PyQt6.QtWidgets import QApplication  # pylint: disable=no-name-in-module

from . import LinkCheckerMain
from .projects import ProjectExt


def excepthook(window, etype, evalue, tb):
    """Catch unhandled exceptions."""
    from io import StringIO
    from linkcheck.director.console import internal_error
    out = StringIO()
    internal_error(out=out, etype=etype, evalue=evalue, tb=tb)
    # signal main window to be thread-safe
    window.error_signal.emit(out.getvalue())


def main(argv=None):
    """Initialize the Qt application, handle commandline arguments
    and show the main window."""
    if argv is None:
        argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName(configuration.AppName)
    app.setApplicationVersion(configuration.Version)
    app.setOrganizationName(configuration.Author)
    args = app.arguments()
    mainkwargs = {}
    if len(args) > 1:
        fileorurl = args[1]
        if is_readable(fileorurl) and fileorurl.lower().endswith(ProjectExt):
            mainkwargs["project"] = fileorurl
        else:
            mainkwargs["url"] = fileorurl
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # use local variable here to avoid garbage collection of the main
    # window before app.exec() finishes
    window = LinkCheckerMain(**mainkwargs)
    window.show()
    window.raise_()  # this will raise the window on Mac OS X
    drop_privileges()
    sys.excepthook = lambda etype, evalue, tb: excepthook(window, etype, evalue, tb)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
