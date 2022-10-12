build:
	make -C lib build
	touch build

test: build
	make -C lib test

install: build
	mkdir -p $(DESTDIR)/usr/lib/teaiso || true
	mkdir -p $(DESTDIR)/usr/bin/teaiso || true
	make -C lib install DESTDIR=`realpath $(DESTDIR)`
	cp -prfv src/* $(DESTDIR)/usr/lib/teaiso/
	cp -prfv profiles $(DESTDIR)/usr/lib/teaiso/
	chmod +x -R $(DESTDIR)/usr/lib/teaiso/
	install mkteaiso $(DESTDIR)/usr/bin/mkteaiso

clean:
	make -C lib clean
	rm -f build

uninstall: clean
	rm -rfv $(DESTDIR)/usr/bin/mkteaiso
	rm -rfv $(DESTDIR)/usr/lib/teaiso/
