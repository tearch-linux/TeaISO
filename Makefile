DESTDIR=/

all:

install:
	mkdir -p $(DESTDIR)/usr/lib/ || true
	mkdir -p $(DESTDIR)/usr/bin/ || true

	install -m 755  mkteaiso $(DESTDIR)/usr/bin/ # Copy app
	cp -prvf profiles $(DESTDIR)/usr/lib/teaiso
	install -m 755  debian.py $(DESTDIR)/usr/lib/teaiso # Copy debian
	install -m 755  archlinux.py $(DESTDIR)/usr/lib/teaiso # Copy debian

install-hooks:
	mkdir -p $(DESTDIR)/usr/lib/ || true
	cp -prvf initcpio $(DESTDIR)/usr/lib/ # Copy initcpio hooks
