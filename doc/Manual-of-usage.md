Teaiso Manual
======

**The ISO generation tool for GNU/Linux**

## About the program

The main program is `mkteaiso`, the program will produce an ISO boot image file and must be parse a default profile (a template Linux flavor) to produce. 

The complete terminology and step by step documentation are into [Teaiso-technology.md](Teaiso-technology.md).

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
 
#### Profiles
 
The profiles are **directories that provides the nature of ISO that will be created**, the format is well described in the document [creating-profile.rst](creating-profile.rst).

These are the available **templates for each supported ["distro" (Linux distribution](Teaiso-technology.md#terminology) base [profile](Teaiso-technology.md#profiles-definitions)**:

| Template name | Profile distro  | observations                 |
| ------------ | ---------------- | ---------------------------- |
| alpine       | Alpine Linux     | power of x86_64 minimal 280MB console image 😳 |
| archlinux    | Arch             | popular x86_64 base image 😒 |
| debian       | Debian GNU/Linux | powered x86_64 testing Debian image 😎  |
| none         | dummy template   | mostly used by debugging 😍 |
| sulin        | Sulin OS linux   | like LFS but with multilib support 😱 |
| tearch       | Arch             | intent to customize to newbie users 😒 |
| ubuntu       | Debian/Ubuntu    | imagine live without casper file.. 😂 |


You must [create a profile](creating-profile.rst) from these templates running the following command: 

`mkteaiso -c <Template name>`

After that, one directory with the name of the `<Template name>` will be created, based on the [profile "distro" definitions](porting-distribution.rst) and [profile format](creating-profile.rst).

You must tune the contents of the directory profile before produce the ISO image. For that get into the `<Template name>` directory just created and edit each file using the [Teaiso technology directives](Teaiso-technology.md).

#### Making the ISO image

To produce a ISO image file based on your directory profile, you must run the following command:

`mkteaiso -c <absolute path of the created profile directory>`

Using your customized profile you can change the name of the profile directory to handle various flavours.

A brief example of making quick ISO its provided at the [starting-use-case.md](starting-use-case.md#customization-example)

#### Debug your process

You can just run the command and will provide standard out of the progress, also a log file is send to the `/var/log/teaiso.log` file. Extra debug information can be obtained by the `--debug` option.

The process uses [stages to determine the progress](Teaiso-technology.md#stage-runlevels) of the creation, 
so in each one some task are performed.

## See also

* [starting-use-case.md](starting-use-case.md)
* [Teaiso-technology.md](Teaiso-technology.md)
