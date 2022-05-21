Teaiso FAQ and Notes
=======

**The ISO generation tool for GNU/Linux**

## Notes

#### Social networks

This project has a active telegram group: https://t.me/iso_calismalari Main language is Turkish but allowed English too. The Tearch linux are a related group comunity https://t.me/TeArchlinux

* Açıklama ve kurallar https://t.me/kurallartr
* GNU/Linux gurubumuz: https://t.me/gnulinuxtr

#### Who are using teaiso?

* **Tearch Linux ISOS**: This project is widely used to produce the [TeArchlinux Releases](https://github.com/tearch-linux/releases) and is part of the [TeArchlinux Project](https://tearch-linux.github.io/)
* **VenenuX Alpine ISOS**: This project is widely used to produce the VenenuX Alpine ISOs https://codeberg.org/alpine/alpine-isomaker using their own forked version https://gitlab.com/venenux/venenux-teaiso
* **PUFF OS ISOS**: This project is widely used to produce the [PUFFOS releases](https://github.com/PuffOS/teaiso-profile/releases/) and have they own forked profile definition.

## FAQ

#### How can i install my Teaiso images?

Teaiso is just a Live ISO image creator, each installer of each Linux flavor are out of scope of the project, you have two options:

- Use the own Live ISO creation tool of each Linux distribution (that of course are more complicated 😌)
- Use the [17g installer](http://gitlab.com/ggggggggggggggggg/17g) a fork of LMDE installer

In some special cases, due the installer nature are included in the rootfs, installation 
can be posible (by example Alpine script `setup-alpine` will work, check next FAQ item)

#### My ISO do not have networking!

Some cases are special, by example alpine init system is complete overridden, so the normal 
init process is not the same, that's the reason `teaiso` created images of alpine linux 
only has networking if you included `networkmanager` package in the live iso creation.

#### Usage of DESTDIR at install

Please understand that although you can set `$DESTDIR` at installation procedure, 
the developer must set paths to the root, and this variable is only used to manage 
the destination of files when performed the install, not the execution of the program.

#### Grub notes

Teaiso uses grub for the creation of the ISO images, so it will install or will need the full Grub suite. 
For example, this means that if you install Teaiso and you don't have grub-firmware on Debian, 
it will be installed or will be required. This is only for the creation of the ISO boot not for the Live Disk roofs.

## See also:

* [Teaiso-technology.md](Teaiso-technology.md)
