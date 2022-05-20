Teaiso INSTALL
==============

**The ISO generation tool for GNU/Linux**

## Requirements

Currently **Teaiso** is not packaged in any distro, but is distribution agnostic.. 
so will work in any linux distro, including those with `muslc` library.

Just the program does not need RAM neither DISK so much.. but when performed runtime 
will need so much as you wants into each iso generation.

## Dependencies

#### Build

* git
* wget
* gcc
* make

#### Runtime

* bash
* chroot
* coreutils
* python3
* busybox
* mtools
* xorriso
* grub (check issue #3)
* squashfs-tools

## Installation

The installation only places files in two places, for more information review [Teaiso technology paths](Teaiso-technology.md#paths)

Please read about the [usage of `$DESTDIR` variable at FAQ-and-notes.md](FAQ-and-notes.md#usage-of-destdir-at-install).

#### Local install

This is the recommended way for any kind of linux:

```
git clone https://gitlab.com/tearch-linux/applications-and-tools/teaiso

cd teaiso

make build

make install
```

#### Network install

This is only valid for Debian based distributions. Basically performs in automatic way the local install.

```
wget https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/raw/master/netinstall -O - | bash
```

## See also:

* [README.md](README.md)
