DESTDIR=/

all:

install:
	mkdir -p $(DESTDIR)/usr/lib/ || true
	mkdir -p $(DESTDIR)/usr/bin/ || true
	mkdir -p $(DESTDIR)/usr/lib/teaiso/efi/ || true

	install -m 755  mkteaiso $(DESTDIR)/usr/bin/ # Copy app
	cp -r efi/* $(DESTDIR)/usr/lib/teaiso/efi
	cp -prvf profiles $(DESTDIR)/usr/lib/teaiso
install-hooks:
	mkdir -p $(DESTDIR)/usr/lib/ || true
	cp -prvf initcpio $(DESTDIR)/usr/lib/ # Copy initcpio hooks
