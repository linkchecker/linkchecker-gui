# Copyright (C) 2011-2016 Bastian Kleineidam
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
"""Provide custom validators."""

from PyQt6 import QtGui
import re


def check_regex(value):
    """Check if given string value can be compiled with re.compile()."""
    try:
        re.compile(value)
    except re.error:
        return False
    else:
        return True


class PyRegexValidator(QtGui.QValidator):
    """Validate input that it is a valid Python regular expression."""

    def validate(self, input, pos):
        if check_regex(input):
            return (QtGui.QValidator.State.Acceptable, pos)
        return (QtGui.QValidator.State.Intermediate, pos)

    def fixup(self, input):
        while not check_regex(input):
            input.chop(1)
