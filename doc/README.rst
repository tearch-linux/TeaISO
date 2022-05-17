Teaiso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**The ISO generation tool for GNU/Linux**

About Teaiso
============

This is just a Live ISO generator, but wait! **It's not what you think! It generates any linux iso in a simple way**, with a generic method.

The mayor feature its that **produces ISO of any kind of linux distribution** as base.

The simplest equivalent is Debian's `live-build`, but without so many complications, just add packages, create the iso starting mechanisms, but without changing the nature of the base distro to be generated.

About the project
============

**Teaiso** is the iso generation tool of the **Tearch-linux** project at https://gitlab.com/tearch-linux, our goal is not being distro like `eos`, `arco`.

About the technology
============

Our technology is made with `c`, `bash` and `python`, the work of the teaiso is using chroot by the moment, in the future we will reimplement in `vala` and maybe use docker containers to avoid touch system process.

The live system used the `squashfs-tools` to produce the rootfs we called `airootfs` where we put everything included for live stuffs like desktop sesion.

The project uses the concept of "profiles" as linux distributions to build, each profile are few files that determines what customizations are made in live mode and what stuffs are included in the squasfs file.

Where to starting
============

Currently **Teaiso** is not packaged in any distro, but is distribution agnostic.. just clone the repository and install as described.

When you install the project, only two places are touch, the program binary (the script named `mkteaiso`) that wil be in `$(DESTDIR)/usr/bin/mkteaiso` and the scripts files that will be in `$(DESTDIR)/usr/lib/teaiso/` as default paths when installed. For more information check the INSTALL.md file of the root directorty of the project sources.

After that just call `mkteaiso` with a profile to build default linux distro. For more information of usage check [starting-use-case.md](starting-use-case.md)


See also
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* [doc/starting-use-case.md](doc/starting-use-case.md)
* [creating-profile](creating-profile.rst)
* [porting-distribution](porting-distribution.rst)
