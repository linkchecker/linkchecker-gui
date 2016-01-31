MANHTMLFILES:= \
	$(HTMLDIR)/man1/linkchecker-gui.1.html

MANFILES:=linkchecker-gui.1
LOCALES:=en de

all:

po4a:
	po4a --localized-charset=UTF-8 po4a.conf

man:	$(MANHTMLFILES)

# check all makefiles for formatting warnings
check:
	@t=$(shell tempfile); \
	for loc in $(LOCALES); do \
	  for manfile in $(MANFILES); do \
	    echo "Checking $$loc/$$manfile"; \
	    LC_ALL=en_US.UTF-8 MANWIDTH=80 man --warnings -E UTF-8 -l $$loc/$$manfile > /dev/null 2>$$t ; \
	    if [ -s $$t ]; then cat $$t; exit 1; fi; \
	  done; \
	done

.PHONY: po4a man check
