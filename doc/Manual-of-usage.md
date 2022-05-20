Teaiso Manual
======

**The ISO generation tool for GNU/Linux**

## About the program

The main program is `mkteaiso`, the program will produce an ISO boot image file and must be parse a default profile (linux flavour) to produce. 
-
-The complete terminology and step by step documentation are into [teaiso-technology.md](teaiso-technology.md).
-
-For quick workflow, first lest check what profiles (linux flavours) we can produce:

## Help of the program
-
-```
-Usage: mkteaiso -p=PROFILE [OPTION]...
-ISO generation tool for GNU/Linux.
-Example: mkteaiso -p=/usr/lib/teaiso/profiles/archlinux --interactive
-Profile directory should contain profile.yaml.
-
-Base Arguments:
-  -p=PROFILE, --profile=PROFILE     Profile directory or name (default: archlinux)
-  -o=OUTPUT, --output=OUTPUT        ISO output directory (default: /var/lib/teaiso/output)
-  -w=WORK, --work=WORK              ISO work directory (default: /var/lib/teaiso/work)
-  -c=BASE, --create=BASE            Create profile by base profile
-  -g=KEY, --gpg=KEY                 Sign airootfs image by GPG
-
-Miscellaneous:
-  -h, --help                        Display this help text and exit
-      --version                     Display version and exit
-      --nocolor                     Disable colorized output
-      --simulate                    Enable simulation mode
-      --nocheck                     Skip all check
-      --interactive                 Interactive operations
-      --debug                       Enable debug mode
-```
 


 #### Profiles
 
-The profiles are the flavours of iso that will be created, the format is well described in the document [creating-profile.rst](creating-profile.rst).
-
-These are the available profiles and defaults for each one:
