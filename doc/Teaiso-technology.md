Teaiso technology
==================

**The ISO generation tool for GNU/Linux**

##  General information

Our project is made with `c`, `bash` and `python`, the work of the teaiso is using chroot by the moment.

The live system used the `squashfs-tools` to produce the rootfs of the live disk.

The project uses the concept of "[profiles](#profiles-definitions)" as linux distributions to build, 
each profile are few files that determines what customizations are made in live mode 
and what stuffs are included in the squasfs file; also each [profile](#profiles-definitions) 

#### Terminology

* `airootfs`: is the rootfs directory that willwork and from the squasfs will be created.
* `profile`: are directories where customizations will be taken to apply over the `airootfs` check [Profile definitios](#profiles-definitions) section for information.
    * skeleton profiles: are template base from the teaiso profile directory, use it for creation of working profiles.
    * working profiles: are the real profiles created based on the skeleton ones. and will handle customizations to apply.
* `distro`: each profile corresponds to a distro script for processing, to perform specific distro needs, check [porting-distribution.rst](porting-distribution.rst) for more information.
    * `funtion`: the distro format defined functions that will determine modifications and actions over the `airootfs`.
    * `variables`: are used in the performed funtions only for some distros, by example Debian based ones.
* `shared`: this is a directory that will be common beetween the `airootfs` and the host real filesystem
* `stage`: the runlevels controls to determine the creation progress of the iso generation, [we have 10 stage runlevels](#stage-runlevels) where the [profile customizations](#profiles-definitions) will be apply.
* `mkteaiso`: is the main program to use, check the quick workflow at the [starting-use-case.md](starting-use-case.md) document.

#### Artifacts

| stuff      | path                         | notes |
| ---------- | ---------------------------- | ----- |
| `mkteaiso` | `$(DESTDIR)/usr/bin`         | Its the main program |
| teaiso     | `$(DESTDIR)/usr/lib/teaiso`  | teaiso files artifacs |
| outputs    | `/var/lib/teaiso`            | teaiso product outputs |
| logs       | `/var/log/teaiso.log`        | teaiso trace outputs |

#### Paths

When you [install](Installation.md) the project, only two places are touch, 
the program binary named `mkteaiso` that will be in `$(DESTDIR)/usr/bin` 
and the program files that will be in `$(DESTDIR)/usr/lib/teaiso/` when installed.
Please read about the [usage of `$DESTDIR` variable at FAQ-and-notes.md](FAQ-and-notes.md#usage-of-destdir-at-install).

When you [used]() the program, extra path will be used, 
the program works and outputs the iso images at `/var/lib/teaiso/`. 
the working dirs will be at `/var/lib/teaiso/work`. and 
the output iso files will be at `/var/lib/teaiso/output`.
The logs will be performed also into `/var/log`.

The output and work paths are cutomizable, those are not auto cleaned by the program, 
neither managed by uninstal.

#### Stage runlevels

The stage runlevels controls to determine the creation progress of the iso generation, 
we have 10 stage runlevels where the profile customizations will be apply:

* 0 This performs the cofnigurations and check
* 1 This performs the init from the distro definition, special case are handle by example in alpine and debian.
* 2 This performs the population of the `airootfs` and the mount of the shared directory parsed to the `mkteaiso` command
* 3 This performs the customizations of the `airootfs` by running `customize_airootfs_pre` script of `profile` definition
* 4 This performs the installation of base rootfs packages of `distro` using "packages" file of `profile`
* 5 This performs the preparation of the customized `airootfs` in the working dir for post customizations
* 6 This performs the customizations of the `airootfs` by running the `customize_airootfs` script of `profile` definition
* 7 This performs the list of the packages installed for information, and later umount the shared directory
* 8 This performs the file permission by lines defined in `file_permission` field of `profile` definition, after that creates the `squashfs` file
* 9 This performs the creation of the iso image after customizations made by the `customize_isowork` scripts, will handle the `squashfs` file

#### Variables

TODO

## Profiles definitions

Those are directories where customizations will be taken to apply over the `airootfs` 
check [creating-profile.rst](creating-profile.rst) for more information.

## Customizations scripts 

The contents of the iso are manage on two filesystems, the root OS and the ISO file.
Those scripts are just **pure bash format but limited in context by the nature of the running `stage` environment**.

* `customize_airootfs_pre` will perform all those command before put packages of `distro` using "packages" file of `profile`
* `customize_airootfs` will perform all those command after put packages of `distro` using "packages" file of `profile`
* `customize_isowork_pre` will perform all those command before creation of the ISO image
* `customize_isowork` will perform all those command at the creation of the ISO image, but not before

## See also

* [starting-use-case.md](starting-use-case.md)
* [creating-profile](creating-profile.rst)
* [porting-distribution](porting-distribution.rst)
