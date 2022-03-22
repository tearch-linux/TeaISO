# Teaiso
```
Usage: mkteaiso -p=PROFILE [OPTION]...
ISO generation tool for GNU/Linux.
Example: mkteaiso -p=/usr/lib/teaiso/profiles/archlinux --interactive
Profile directory should contain profile.yaml.

Base Arguments:
  -p=PROFILE, --profile=PROFILE     Profile directory or name (default: archlinux)
  -o=OUTPUT, --output=OUTPUT        ISO output directory (default: /var/teaiso/output)
  -w=WORK, --work=WORK              ISO work directory (default: /var/teaiso/work)
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

## Documentation: 
Please visit **doc** directory.

## Installation

`make` and `make install`

## Netinstall
Run as root:
`wget https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/raw/master/netinstall -O - | bash`

## Dependencies
* gcc (build)
* make (build)
* python3
* busybox
* mtools
* xorriso
* grub (for creating iso)
* squashfs-tools
