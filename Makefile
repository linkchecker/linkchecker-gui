# This Makefile is only used by developers.
PYVER:=2.7
PYTHON?=python$(PYVER)
VERSION:=$(shell $(PYTHON) setup.py --version)
APPNAME:=$(shell $(PYTHON) setup.py --name)
PY_FILES_DIRS:=linkcheck_gui tests *.py linkchecker-gui
MYPY_FILES_DIRS:=linkcheck_gui/__init__.py \
	  linkcheck_gui/checker.py \
	  linkcheck_gui/contextmenu.py \
	  linkcheck_gui/debug.py \
	  linkcheck_gui/editor.py \
	  linkcheck_gui/editor_qsci.py \
	  linkcheck_gui/editor_qt.py \
	  linkcheck_gui/lineedit.py \
	  linkcheck_gui/help.py \
	  linkcheck_gui/logger.py \
	  linkcheck_gui/options.py \
	  linkcheck_gui/properties.py \
	  linkcheck_gui/settings.py \
	  linkcheck_gui/statistics.py \
	  linkcheck_gui/syntax.py \
	  linkcheck_gui/urlmodel.py \
	  linkcheck_gui/urlsave.py \
	  linkchecker-gui \
	  *.py

TESTS ?= tests
# set test options, eg. to "--verbose"
TESTOPTS=

all:
	@echo "Read the file doc/install.txt to see how to build and install this package."

clean:
	-$(PYTHON) setup.py clean --all
	$(MAKE) -C doc/html clean
	find . -name '*.py[co]' -exec rm -f {} \;
	find . -depth -name '__pycache__' -exec rm -rf {} \;

distclean: clean
	rm -rf build dist $(APPNAME).egg-info

locale:
	$(MAKE) -C po

dist: locale
	[ -d dist ] || mkdir dist
	$(PYTHON) setup.py sdist --formats=tar bdist_wheel
	gzip --best dist/$(APPNAME)-$(VERSION).tar

# The check programs used here are mostly local scripts on my private system.
# So for other developers there is no need to execute this target.
check:
	check-copyright
	check-pofiles -v
	py-tabdaddy $(MYPY_FILES_DIRS)
	py-unittest2-compat tests/
	$(MAKE) -C doc check
	$(MAKE) doccheck
	$(MAKE) pyflakes

doccheck:
	py-check-docstrings --force $(MYPY_FILES_DIRS)

update-copyright:
	update-copyright --holder="Bastian Kleineidam" $(PY_FILES_DIRS) doc

test:
	env LANG=en_US.utf-8 PYTHONPATH=$(HOME)/projects/linkchecker.git $(PYTHON) -m pytest $(TESTOPTS) $(TESTS)

pyflakes:
	pyflakes $(PY_FILES_DIRS) 2>&1 | \
          grep -v -E "'PyQt4' imported but unused" | \
          grep -v "undefined name '_'" | \
	  grep -v "undefined name '_n'" | cat

gui:
	$(MAKE) -C linkcheck_gui

.PHONY: test gui pyflakes all clean distclean
.PHONY: locale update-copyright chmod dist
