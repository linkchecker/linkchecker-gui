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
import os
import pytest


class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated."""

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


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


@memoized
def has_pyqt():
    """Test if PyQT is installed."""
    try:
        import PyQt5  # noqa: F401

        return True
    except ImportError:
        pass
    return False


need_pyqt = _need_func(has_pyqt, "PyQT")


@memoized
def has_x11():
    """Test if DISPLAY variable is set."""
    return os.getenv('DISPLAY') is not None


need_x11 = _need_func(has_x11, 'X11')


if __name__ == '__main__':
    print("has PyQt", has_pyqt())
    print("has X11", has_x11())
