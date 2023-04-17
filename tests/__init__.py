# Copyright (C) 2005-2016 Bastian Kleineidam
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

from functools import lru_cache
import os

import pytest


def _need_func(testfunc, name):
    """Decorator skipping test if given testfunc fails."""

    def check_func(func):
        def newfunc(*args, **kwargs):
            if not testfunc():
                pytest.skip("%s is not available" % name)
            return func(*args, **kwargs)
        newfunc.__name__ = func.__name__
        return newfunc

    return check_func


@lru_cache(1)
def has_pyqt():
    """Test if PyQT is installed."""
    try:
        import PyQt6  # noqa: F401

        return True
    except ImportError:
        pass
    return False


need_pyqt = _need_func(has_pyqt, "PyQT")


@lru_cache(1)
def has_x11():
    """Test if DISPLAY variable is set."""
    return os.getenv('DISPLAY') is not None


need_x11 = _need_func(has_x11, 'X11')


if __name__ == '__main__':
    print("has PyQt", has_pyqt())
    print("has X11", has_x11())
