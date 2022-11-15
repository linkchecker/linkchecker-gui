#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
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
from __future__ import print_function
import sys
if not (hasattr(sys, 'version_info') or
        sys.version_info < (2, 7, 0, 'final', 0)):
    raise SystemExit("This program requires Python 2.7 or later.")
import os

# import Distutils stuff
from setuptools import setup

# the application version
AppVersion = "9.4"
# the application name
AppName = "LinkCheckerGUI"
Description = "GUI for LinkChecker"


myname = "Bastian Kleineidam"
myemail = "bastian.kleineidam@web.de"

data_files = [
    ('share/linkchecker',
        ['doc/html/lccollection.qhc', 'doc/html/lcdoc.qch']),
]

if os.name == 'posix':
    data_files.append(('share/man/man1', ['doc/en/linkchecker-gui.1']))
    data_files.append(('share/man/de/man1', ['doc/de/linkchecker-gui.1']))
    data_files.append(('share/applications', ['doc/linkchecker-gui.desktop']))

args = dict(
    name = AppName,
    version = AppVersion,
    description = Description,
    author = myname,
    author_email = myemail,
    maintainer = myname,
    maintainer_email = myemail,
    url = "https://github.com/wummel/linkchecker-gui",
    license = "GPL",
    packages = [
        'linkcheck_gui',
    ],
    scripts = ['linkchecker-gui'],
    data_files = data_files,
    classifiers = [
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
    ],
    install_requires=[
        'linkchecker>=9.4',
        #'PyQt4', # install from http://www.riverbankcomputing.com/software/pyqt/download
    ],
)
setup(**args)
