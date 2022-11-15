HELPFILES := lccollection.qhc
HTMLFILES := index.html
ICOICONS := logo/16x16/linkchecker-gui.png logo/32x32/linkchecker-gui.png
ICNSICONS := logo/16x16/linkchecker-gui.png logo/32x32/linkchecker-gui.png logo/48x48/linkchecker-gui.png logo/128x128/linkchecker-gui.png

all:	$(HELPFILES) $(HTMLFILES)

clean:
	-rm -f *.qhc *.qch

%.html:	%.txt html.header html.footer
	(cat html.header; markdown2 $<; cat html.footer) > $@

test:
	xmllint --valid --noout $(HTMLFILES)

%.qhc:	%.qhcp lcdoc.qhp $(HTMLFILES)
	-qcollectiongenerator $< -o $@

favicon.ico:	$(ICOICONS)
	png2ico favicon.ico $(ICOICONS)

favicon.icns:	$(ICNSICONS)
	png2icns favicon.icns $(ICNSICONS)

.PHONY: clean test
