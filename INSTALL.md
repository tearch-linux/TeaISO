Teaiso INSTALL
==============

**The ISO generation tool for GNU/Linux**

## Requirements

Currently **Teaiso** is not packaged in any distro, but is distribution agnostic.. so will work in any linux distro, including those with muslc. For more information check [docs](docs) directory.

#### Build

* git
* wget
* gcc
* make

#### Dependencies

* chroot
* python3
* busybox
* mtools
* xorriso
* grub (check issue #3)
* squashfs-tools

## Installation

When you install the project, only two places are touch, the program binary (the script named `mkteaiso`) that will be in `$(DESTDIR)/usr/bin/mkteaiso` and the program files that will be in `$(DESTDIR)/usr/lib/teaiso/` as default paths when installed.

#### Local install

`make` and `make install DESTDIR=/usr`

#### Network install

Run as root:
`wget https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/raw/master/netinstall -O - DESTDIR=/usr | bash DESTDIR=/usr `

## See also:

* [README.md](README.md)
* [doc/starting-use-case.md](doc/starting-use-case.md)
