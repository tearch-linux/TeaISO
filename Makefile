DESTDIR=/

all: install

install:
	mkdir -p $(DESTDIR)/usr/lib/ || true
	mkdir -p $(DESTDIR)/usr/bin/ || true
	mkdir -p $(DESTDIR)/usr/lib/teaiso/efi/ || true

	cp -prvf initcpio $(DESTDIR)/usr/lib/ # Copy initcpio hooks
	install -m 755  mkteaiso $(DESTDIR)/usr/bin/ # Copy app
	cp -r efi/* $(DESTDIR)/usr/lib/teaiso/efi
	cp -prvf profiles $(DESTDIR)/usr/lib/teaiso
