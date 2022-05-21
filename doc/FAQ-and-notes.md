Teaiso FAQ and Notes
=======

**The ISO generation tool for GNU/Linux**

## Notes

#### Social networks

This project has a active telegram group: https://t.me/iso_calismalari Main language is Turkish but allowed English too. The Tearch linux are a related group comunity https://t.me/TeArchlinux

* Açıklama ve kurallar https://t.me/kurallartr
* GNU/Linux gurubumuz: https://t.me/gnulinuxtr

This project is widelly used to produce the VenenuX Alpine ISOS https://codeberg.org/alpine/alpine-isomaker usign their own forked version https://gitlab.com/venenux/venenux-teaiso

## FAQ

#### How can i install my teaiso images

Teaiso is just a Live ISO image creator, the each linux installers are out of scope of the project, you have two options:

- Use the distro Live ISO creation tool (that of course are more complicated 😌)
- Use the [17g installer](http://gitlab.com/ggggggggggggggggg/17g) a fork of LMDE installer

In some special cases, due the installer nature are included in the rootfs, installation 
can be posible (by example Alpine script `setup-alpine` will work, check nexd faq item)

#### My iso do not have networking

Some cases are special, by example alpine init system is complete overriden, so the normal 
init process is not the same, that's the reason `teaiso` created images of alpine linux 
only has networking if you included `networkmanager` package in the live iso creation.

#### Usage of DESTDIR at install

Please understand that although you can set `$DESTDIR` at installation procedure, 
the developer has set paths to the root, and this variable is only used to manage 
the destination of files when performed the install, not the execution of the program.

## See also:

* [Teaiso-technology.md](Teaiso-technology.md)
