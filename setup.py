#!/usr/bin/python3
# Copyright (C) 2016 Bastian Kleineidam
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
Setup file for the distuils module.

It includes the following features:
- creation and installation of configuration files with installation data
- automatic MANIFEST.in check
- automatic generation of .mo locale files
- automatic permission setting on POSIX systems for installed files
"""

import sys

if sys.version_info < (3, 5, 0, 'final', 0):
    raise SystemExit("This program requires Python 3.5 or later.")
import os

# import Distutils stuff
from setuptools import find_packages, setup

# the application version
AppVersion = "10.0a1.dev0"
# the application name
AppName = "LinkCheckerGUI"
Description = "GUI for LinkChecker"


myname = "Bastian Kleineidam"
myemail = "bastian.kleineidam@web.de"


def get_icons():
    icons = []
    for size in 16, 32, 48, 64, 128:
        icons.append(('share/icons/hicolor/{0}x{0}/apps'.format(size),
                     ['doc/html/logo/{0}x{0}/linkchecker-gui.png'.format(size)]))
    return icons


data_files = []  # XXX
#    ('share/linkchecker', ['doc/html/lccollection.qhc', 'doc/html/lcdoc.qch'])
# ]

if os.name == 'posix':
    data_files.append(('share/man/man1', ['doc/en/linkchecker-gui.1']))
    data_files.append(('share/man/de/man1', ['doc/de/linkchecker-gui.1']))
    data_files.append(('share/applications', ['doc/linkchecker-gui.desktop']))
    data_files.extend(get_icons())

args = dict(
    name=AppName,
    version=AppVersion,
    description=Description,
    author=myname,
    author_email=myemail,
    maintainer=myname,
    maintainer_email=myemail,
    url="https://github.com/linkchecker/linkchecker-gui",
    license="GPL",
    packages=find_packages(include=["linkcheck_gui", "linkcheck_gui.*"]),
    entry_points={
        "gui_scripts": ["linkchecker-gui = linkcheck_gui.__main__:main"],
    },
    data_files=data_files,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
    ],
    install_requires=[
        "importlib_metadata;python_version<'3.8'",
        "linkchecker>=10.1",
        "PyQt5",
    ],
)
setup(**args)
