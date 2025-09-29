# Copyright (C) 2006-2014 Bastian Kleineidam
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
Output debugging information for an error.
"""
import os
import sys
import time

import linkcheck

from .. import configuration


def print_env_info(key, out):
    """If given environment key is defined, print it out."""
    value = os.getenv(key)
    if value is not None:
        print(key, "=", repr(value), file=out)


def print_app_info(out):
    """Print system and application info."""
    print(_("System info:"), file=out)
    print(configuration.App, file=out)
    print(_("Released on:"), configuration.ReleaseDate, file=out)
    print(
        _("Python %(version)s on %(platform)s")
        % {"version": sys.version, "platform": sys.platform},
        file=out,
    )
    print(f"LinkChecker {linkcheck.configuration.Version}", file=out),
    print(configuration.get_modules_info(), file=out)
    stime = linkcheck.strformat.strtime(time.time())
    print(_("Local time:"), stime, file=out)
    print(_("sys.argv:"), sys.argv, file=out)


def print_proxy_info(out):
    """Print proxy info."""
    for key in ("http_proxy", "https_proxy", "curl_ca_bundle", "no_proxy"):
        print_env_info(key, out=out)


def print_locale_info(out):
    """Print locale info."""
    for key in ("LANGUAGE", "LC_ALL", "LC_CTYPE", "LANG"):
        print_env_info(key, out=out)


def internal_error(out, etype, evalue, tb):
    print(os.linesep, file=out)
    print(_("""********** Oops, I did it again. *************

You have found an internal error in LinkChecker GUI. Please write a bug report
at %s
and include the following information:
- the URL or file you are testing
- the system information below

Not disclosing some of the information above due to privacy reasons is OK.
I will try to help you nonetheless, but you have to give me something
I can work with ;) .
""") % configuration.Url, file=out)
    if etype is None:
        etype = sys.exc_info()[0]
    if evalue is None:
        evalue = sys.exc_info()[1]
    if tb is None:
        tb = sys.exc_info()[2]
    linkcheck.better_exchook2.better_exchook(etype, evalue, tb, out)
    print_app_info(out=out)
    print_proxy_info(out=out)
    print_locale_info(out=out)
    print(
        os.linesep,
        _("******** LinkChecker GUI internal error, over and out ********"),
        file=out,
    )
