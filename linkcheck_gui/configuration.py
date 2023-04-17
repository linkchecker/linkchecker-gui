# Copyright (C) 2000-2014 Bastian Kleineidam
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
Store metadata and options.
"""

from linkcheck import fileutil

try:
    from . import _release
except ImportError:
    raise SystemExit('Run "hatchling build --hooks-only" first')

Version = _release.__version__
ReleaseDate = _release.__release_date__
CopyrightYear = _release.__copyright_year__
AppName = _release.__app_name__
App = AppName + " " + Version
Author = _release.__author__
HtmlAuthor = Author.replace(' ', '&nbsp;')
Copyright = f"Copyright (C) 2012-2016 Bastian Kleineidam, 2017-{CopyrightYear} {Author}"
HtmlCopyright = (
    "Copyright &copy; 2012-2016 Bastian&nbsp;Kleineidam, "
    f"2017-{CopyrightYear} {HtmlAuthor}")
HtmlAppInfo = App + ", " + HtmlCopyright
Url = _release.__url__
Freeware = (
    AppName
    + """ comes with ABSOLUTELY NO WARRANTY!
This is free software, and you are welcome to redistribute it under
certain conditions. Look at the file `LICENSE' within this distribution."""
)


# List Python modules in the form (module, name, version attribute)
Modules = (
    # required modules
    ("PyQt6.QtCore", "PyQt6", "PYQT_VERSION_STR"),
    ("PyQt6.Qsci", "QScintilla", "QSCINTILLA_VERSION_STR"),
)


def get_modules_info():
    """Return unicode string with detected module info."""
    module_infos = []
    for (mod, name, version_attr) in Modules:
        if not fileutil.has_module(mod):
            continue
        if version_attr and hasattr(mod, version_attr):
            attr = getattr(mod, version_attr)
            version = attr() if callable(attr) else attr
            module_infos.append(f"{name} {version}")
        else:
            # ignore attribute errors in case library developers
            # change the version information attribute
            module_infos.append(name)
    return "Modules: %s" % (", ".join(module_infos))
