# LinkChecker-GUI

[![GPL-3](https://img.shields.io/badge/license-GPL3-d49a6a.svg)](https://opensource.org/licenses/GPL-3.0)

This is the GUI client for [LinkChecker](https://linkchecker.github.io/linkchecker/).

## Installation

Python 3.9 or later is needed. Using pip to install LinkChecker-GUI:

`pip3 install linkchecker-gui`

You may wish to first install the dependencies from you distribution e.g.:

`apt install linkchecker python3-pyqt6.qsci python3-pyqt6.qthelp`

The version in the pip repository may be old, to install the latest code first
install qhelpgenerator e.g.

`apt install qt6-documentation-tools`

Then:

`pip3 install https://github.com/linkchecker/linkchecker-gui/archive/master.tar.gz`

## Usage

`linkchecker-gui`

A freedesktop.org desktop entry is installed for compatible environments.

On Debian/Ubuntu if LinkChecker-GUI fails to start with an error:

    qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.

this can be resolved by installing libxcb-cursor0:

`apt install libxcb-cursor0`

Recursion depth and verbose output (whether every URL checked is shown or just those with errors)
are configured in Edit/Options. These settings are specific to LinkChecker-GUI and independent
of LinkChecker. More advanced settings are shared with the default LinkChecker linkcheckerrc.

## Development

Development is managed on [GitHub](https://github.com/linkchecker/linkchecker-gui).
