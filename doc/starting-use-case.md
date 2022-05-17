Teaiso brief usage
==================

**The ISO generation tool for GNU/Linux**

##  General usage

The main program is `mkteaiso`, the program will produce an ISO boot image file and must be parse a default profile (linux flavour) to produce. 

The complete terminology and step by step documentation are into [teaiso-technology.md](teaiso-technology.md).

For quick workflow, first lest check what profiles (linux flavours) we can produce:

#### Profiles

The profiles are the flavours of iso that will be created, the format is well described in the document [creating-profile.rst](creating-profile.rst).

These are the available profiles and defaults for each one:

| name         | linux            | observations                 |
| ------------ | ---------------- | ---------------------------- |
| alpine       | Alpine Linux     | power of x86_64 minimal 280MB console image 😳 |
| archlinux    | Arch             | popular x86_64 base image 😒 |
| debian       | Debian GNU/Linux | powered x86_64 testing Debian image 😎  |
| none         | dummy template   | mostly used by debugging 😍 |
| sulin        | Sulin OS linux   | like LFS but with multilib support 😱 |
| tearch       | Arch             | intent to customize to newbie users 😒 |
| ubuntu       | Debian/Ubuntu    | imagine live without casper file.. 😂 |

#### Working dir and space

Profiles will determine what flavour and the contents of the flavour of linux. Inside each profile there's two scripts: `packages.x86_64` and `customize-airootfs.sh` . Those determines the packages that will be installed and modifications to be made respectivelly.

Due to the fact that an ISO file will be produced, a considerable space will be required, this will depend on modifying the file `customize-airootfs.sh` and `packages.x86_64`. If you use default profiles the sizes will be around 300Mb.

 For more information about `mkteaiso` terminology check [teaiso-technology.md](teaiso-technology.md).

#### Default Examples

* To produce a alpine linux base just `mkteaiso -p=alpine`
* To produce a debian linux testing `mkteaiso -p=debian`

The ISO files will be produced to the `/var/lib/teaiso/output` directory, with date as part of the name. For more information about `mkteaiso` workflow check [teaiso-technology.md](teaiso-technology.md)

#### Customization Examples

You can made your own customized iso:

* Create a working directory of the profile and copy base profiles, in this case we will create a KDE based iso but from Alpine defualt profile:

```
mkdir /usr/src/teaiso-alpine-kde-stable

cp /usr/lib/teaiso/profiles/alpine/* /usr/src/teaiso-alpine-kde-stable/
```

* Customize the defaults of the `airootfs` (the root of the installed live files), here we just add kde stuff and provide default password of users:

```

cat > /usr/src/teaiso-alpine-kde-stable/customize-airootfs.sh << EOF
#!/usr/bin/env bash
setup-xorg-base || true
apk add plasma kde-applications-base elogind polkit-elogind dbus
echo -e "live\nlive\n" | passwd root
echo -e "live\nlive\n" | adduser user || true
rc-update add dbus
rc-update add sddm
rc-update add udev
rc-update add elogind
EOF
```

* Finally just run the profile with the program:

```
mkteaiso --profile=/usr/src/teaiso-alpine-kde-stable
```

 For more information about `mkteaiso` check [teaiso-technology.md](teaiso-technology.md).

## Help of the program

```
Usage: mkteaiso -p=PROFILE [OPTION]...
ISO generation tool for GNU/Linux.
Example: mkteaiso -p=/usr/lib/teaiso/profiles/archlinux --interactive
Profile directory should contain profile.yaml.

Base Arguments:
  -p=PROFILE, --profile=PROFILE     Profile directory or name (default: archlinux)
  -o=OUTPUT, --output=OUTPUT        ISO output directory (default: /var/lib/teaiso/output)
  -w=WORK, --work=WORK              ISO work directory (default: /var/lib/teaiso/work)
  -c=BASE, --create=BASE            Create profile by base profile
  -g=KEY, --gpg=KEY                 Sign airootfs image by GPG

Miscellaneous:
  -h, --help                        Display this help text and exit
      --version                     Display version and exit
      --nocolor                     Disable colorized output
      --simulate                    Enable simulation mode
      --nocheck                     Skip all check
      --interactive                 Interactive operations
      --debug                       Enable debug mode
```

## See also

* [teaiso-technology.md](teaiso-technology.md)
* [creating-profile](creating-profile.rst)
* [porting-distribution](porting-distribution.rst)
