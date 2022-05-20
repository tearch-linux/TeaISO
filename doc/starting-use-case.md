Teaiso brief usage
==================

**The ISO generation tool for GNU/Linux**

##  General usage

The main program is `mkteaiso`this document is a quick workflow (for more complete information consult the document [Manual-of-usage.md](Manual-of-usage.md)).

#### Fast Example

To produce a Debian "testing" ISO Linux based on [Debian profile](#profiles):

```
mkteaiso -c debian
cd debian
mkteaiso -p $(pwd)
```

The ISO files will be produced to the `/var/lib/teaiso/output` directory, with date as part of the name.

> This document is a quick way to carry out the workflow, for more complete information consult the document [Manual-of-usage.md](Manual-of-usage.md)

#### Profiles

Firt we must create a [profile](Manual-of-usage.md#profiles), profiles are the template flavours of iso that will be created, based on ["distro"](Teaiso-technology.md#terminology) (supported distributions) like: alpine, debian, etc..

> This document is a quick review made for fast workflow, please check [profile](Manual-of-usage.md#profiles) section of [Manual-of-usage.md](Manual-of-usage.md#profiles).

#### Customization Example

You can made your own customized iso:

* Create a working directory of the profile and copy base profiles, in this case we will create a KDE based iso but from Alpine defualt profile:

```
cd /usr/src

mkteaiso -c alpine

mv alpine teaiso-alpine-kde-stable

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

> For more information about `mkteaiso` terminology check [Teaiso-technology.md](Teaiso-technology.md).


## See also

* [Manual-of-usage.md](Manual-of-usage.md)
* [Teaiso-technology.md](Teaiso-technology.md)
