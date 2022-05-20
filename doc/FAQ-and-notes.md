Teaiso FAQ and Notes
=======

**The ISO generation tool for GNU/Linux**

## Notes

#### Social networks

This project has a active telegram group: https://t.me/iso_calismalari Main language is Turkish but allowed English too.

* Açıklama ve kurallar https://t.me/kurallartr
* GNU/Linux gurubumuz: https://t.me/gnulinuxtr

## FAQ

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
