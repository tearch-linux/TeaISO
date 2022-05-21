Teaiso INSTALL
==============

**The ISO generation tool for GNU/Linux**

## Requirements

Currently **Teaiso** is not packaged in any distribution, but is distribution agnostic.. 
so will work in any Linux distribution, including those with `muslc` or `glibc` library.

The process does not need much RAM neither DISK space.. but when performed runtime 
will need so much as you wants into each ISO generation.

## Requirements

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
* grub ([check notes at FAQ](FAQ-and-notes.md#grub-notes))
* squashfs-tools

## Installation

The installation only places files in two places, for more information review [Teaiso technology paths](Teaiso-technology.md#paths)

Please read about the [usage of `$DESTDIR` variable at FAQ-and-notes.md](FAQ-and-notes.md#usage-of-destdir-at-install).

#### Local install

This is the recommended way for any kind of Linux:

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

* [Manual-of-usage.md](Manual-of-usage.md)
