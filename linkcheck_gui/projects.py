# Copyright (C) 2012-2016 Bastian Kleineidam
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
import re
import os
import shutil
import urllib.parse

from PyQt6 import QtWidgets
from linkcheck.configuration import get_user_config, confparse
from linkcheck.url import default_ports, splitport
from linkcheck.fileutil import is_readable
from .library.fileutil import is_writable

ProjectExt = ".lcp"
ProjectFilter = _("LinkChecker project (*%(ext)s)") % dict(ext=ProjectExt)


class ProjectParser(confparse.LCConfigParser):
    def __init__(self, config, gui_options, urlinput):
        super().__init__(config)
        # has set_options(data) function
        self.gui_options = gui_options
        # has setText(url) function
        self.urlinput = urlinput

    def read(self, files):
        super().read(files)
        self.read_project_config()
        self.read_gui_config()

    def read_project_config(self):
        section = "project"
        if not self.has_section(section):
            return
        option = "url"
        if self.has_option(section, option):
            url = self.get(section, option)
            self.urlinput.setText(url)
        else:
            self.urlinput.setText("")

    def read_gui_config(self):
        section = "gui"
        if not self.has_section(section):
            return
        data = {}
        option = "debug"
        if self.has_option(section, option):
            data[option] = self.getboolean(section, option)
        option = "verbose"
        if self.has_option(section, option):
            data[option] = self.getboolean(section, option)
        option = "recursionlevel"
        if self.has_option(section, option):
            data[option] = self.getint(section, option)
        option = "warninglines"
        if self.has_option(section, option):
            data[option] = self.get(section, option)
        option = "ignorelines"
        if self.has_option(section, option):
            data[option] = self.get(section, option)
        self.gui_options.set_options(data)

    def write(self, fp):
        """Write project configuration to given file object."""
        self.write_project_config()
        self.write_gui_config()
        super().write(fp)

    def write_project_config(self):
        """Write project section configuration."""
        section = "project"
        self.add_section(section)
        self.set(section, "url", self.urlinput.text())

    def write_gui_config(self):
        """Write gui section configuration."""
        section = "gui"
        self.add_section(section)
        for key, value in list(self.gui_options.get_options().items()):
            self.set(section, key, value)


def url_split(url):
    """Split url in a tuple (scheme, hostname, port, document) where
    hostname is always lowercased.
    Precondition: url is syntactically correct URI (eg has no whitespace)
    """
    o = urllib.parse.urlparse(url)
    port = default_ports.get(o.scheme, 0)
    if host := o.netloc:
        host = host.lower()
        host, port = splitport(host, port=port)
    return o.scheme, host, port, o.path


def url_to_filename(url, extension):
    # filter host and document
    parts = url_split(url)
    value = f"{'' if parts[1] is None else parts[1]}{parts[3]}"
    # normalize
    import unicodedata

    value = unicodedata.normalize('NFKD', value)
    # replace non-alpha characters and convert to lowercase
    value = re.sub(r'[^\w-]+', '_', value).strip().lower()
    # add extension
    return value + extension


def saveproject(parent, url):
    """Save a project file."""
    try:
        msg = saveproject_msg(parent, url)
    except Exception as errmsg:
        msg = str(errmsg)
    parent.set_statusmsg(msg)


def saveproject_msg(parent, url):
    """Save a project file and return status message."""
    title = _("Save LinkChecker project")
    func = QtWidgets.QFileDialog.getSaveFileName
    suggestedname = url_to_filename(url, ProjectExt)
    filename, _filter = func(parent, title, suggestedname, ProjectFilter)
    if not filename:
        # user canceled
        return _("Canceled saving a project file.")
    d = dict(filename=filename)
    if not is_writable(filename):
        return _("Could not write project file %(filename)s.") % d
    user_config = get_user_config()
    if is_readable(user_config):
        # Copy user config to filename since this is the current
        # configuration.
        # This way it is not necessary to write the parent.config
        # dictionary back to a file.
        shutil.copy(user_config, filename)
        filter_comments = True
    else:
        # use default config (ie. do not write anything)
        filter_comments = False
    write_header(filename, filter_comments)
    parser = ProjectParser(parent.config, parent.options, parent.urlinput)
    with open(filename, 'a') as fp:
        parser.write(fp)
    return _("Project file %(filename)s saved successfully.") % d


def write_header(filename, filter_comments):
    """Write header and filter comment lines if file already exists."""
    lines = [
        '# This is a generated LinkChecker project file. Do not edit' + os.linesep,
    ]
    if filter_comments:
        with open(filename) as fp:
            for line in fp:
                if not line.lstrip().startswith((';', '#')):
                    lines.append(line)
    with open(filename, 'w') as fp:
        for line in lines:
            fp.write(line)


def openproject(parent):
    """Select and load a project file."""
    try:
        msg = openproject_msg(parent)
    except Exception as errmsg:
        msg = str(errmsg)
    parent.set_statusmsg(msg)


def openproject_msg(parent):
    """Select and load a project file. Returns message to display
    which indicates if file has been loaded successful."""
    title = _("Open LinkChecker project")
    func = QtWidgets.QFileDialog.getOpenFileName
    directory = ""
    filename, _filter = func(parent, title, directory, ProjectFilter)
    if not filename:
        # user canceled
        return _("Canceled opening a project file.")
    if not is_readable(filename):
        return _("Could not read project file %(filename)s.") % dict(filename=filename)
    return loadproject(parent, filename)


def loadproject(parent, filename):
    """Load a project file."""
    try:
        msg = loadproject_msg(parent, filename)
    except Exception as errmsg:
        args = dict(filename=filename, err=errmsg)
        msg = _("Could not load project %(filename)s: %(err)s") % args
    return msg


def loadproject_msg(parent, filename):
    """Load a project file. Returns message to display which indicates if
    file has been loaded successful."""
    parser = ProjectParser(parent.config, parent.options, parent.urlinput)
    parser.read([filename])
    d = dict(filename=filename)
    return _("Project file %(filename)s loaded successfully.") % d
