Teaiso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**The ISO generation tool for GNU/Linux**

## About Teaiso

This is just a Live ISO generator, But wait! **It's not what you think! It generates any iso in a simple way**, with a generic method.

The mayor feature its that **produces ISO of any kind of linux distribution** as base.

The simplest equivalent is Debian's `live-build`, but without so many complications, just add packages, create the iso starting mechanisms, but without changing the nature of the base distro to be generated.

## About the project

Teaiso is the iso generation tool of the Tearch-linux project at https://gitlab.com/tearch-linux cos our goal is not being distro like `eos`, `arco`.

## About the technology

Our technology is made with `c`, `bash` and `python`, the work of the teaiso is using chroot by the moment, in the future we will reimplemnet in `vala` and maybe use docker containers to avoid trast system with chroot zomby process

The live system used the `squashfs-tools` to produce the rootfs we called `airootfs`, were are included all the live stuffs.

The project uses the concept of "profiles" as linux distributions to builds, each profiles describe few files that determines what customizations are made in live mode and what stuff are included in the squasfs file.

## Where to starting

Currently we are not packaged in any distro, but is complety distribution agnostic.. just clone the repository and install as described.

When you install the project, only two places are touch, the program binary (the script named `mkteaiso`) that wil be in `$(DESTDIR)/usr/bin/mkteaiso` and the scripts files that will be in `$(DESTDIR)/usr/lib/teaiso/` as default paths when installed.

After that just call the `mkteaiso` with a profile to build default linux distro of your preference

## See also

* TODO: link more documents here

