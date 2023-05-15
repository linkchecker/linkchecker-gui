# generate Python files from UI description

# edit ui/*.ui files with designer (ie. /usr/bin/designer)
UI_FILES = linkchecker_ui_main.py \
	linkchecker_ui_options.py \
	linkchecker_ui_debug.py \
	linkchecker_ui_editor.py


all: $(UI_FILES)

linkchecker_ui_%.py: ui/%.ui
	pyuic6 -o $@ $<
# replace the Qt translator with the one LinkChecker uses
	sed -i -r -e 's/QtGui\.QApplication\.translate\("[^"]+", "([^"]+)", None, QtGui\.QApplication\.UnicodeUTF8\)/_("\1")/g' $@
# relative import of lineedit
	sed -i -e 's/from lineedit/from .lineedit/' $@

clean:
	rm -f *.pyc *.pyo

rebuild:
	rm -f $(UI_FILES)
	$(MAKE) all
