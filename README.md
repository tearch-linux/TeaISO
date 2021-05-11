# TeaISO

Alternative ISO generation tool for Arch Linux. You can generate UEFI+BIOS (i386-pc, i386-efi, x86_64-efi) compatible ISO images with this tool.


## Usage
    usage: mkteaiso [-h] [-o OUTPUT] [-w WORK] [-c COMPRESSION] [-v] -p PROFILE
    
    ISO creation tool for Arch Linux, v1.1.2
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            Output directory of ISO.
      -w WORK, --work WORK  Work directory of ISOs preparation files.
      -c COMPRESSION, --compression COMPRESSION
                            Compression type of squashfs.
      -v, --verbose         Enable detailed verbose output.
      -p PROFILE, --profile PROFILE
                            Profile directory for ISO.

## Depencies

 - arch-install-scripts
 - dosfstools
 - e2fsprogs
 - grub
 - squashfs-tools
 - mtools
 - libisoburn
 - python
 - python-argparse
 - python-yaml
 - mkinitcpio ***(for mkinitcpio-teaiso)***

Also, you can look at example PKGBUILD by [this link](https://gitlab.com/tearch-linux/packages/tearch-packages/teaiso/-/tree/master).

## Installing
You can install TeaISO by `make DESTDIR=/ install`.

If you want install TeaISO live hooks, you can install by `make DESTDIR=/ install-hooks`

## Example
You can generate examlple *releng ISO* with this command: `mkteaiso -vp /usr/lib/teaiso/profiles/releng/ -w work -o output -c gzip`

## Testing
You can try your ISOs with Qemu+KVM.

 - **x86_64-efi**: `qemu-system-x86_64 -enable-kvm -m 1024 -cdrom output/archlinux-11-05-2021-x86_64.iso -bios /usr/share/edk2-ovmf/x64/OVMF.fd` 
 - **i386-efi**: `qemu-system-x86_64 -enable-kvm -m 1024 -cdrom output/archlinux-11-05-2021-x86_64.iso -bios /usr/share/edk2-ovmf/ia32/OVMF.fd` 
 - **i386-pc**: `qemu-system-x86_64 -enable-kvm -m 1024 -cdrom output/archlinux-11-05-2021-x86_64.iso` 

**Note:** You must install [qemu](https://archlinux.org/packages/extra/x86_64/qemu/) for testing. And you need [edk2-ovmf](https://archlinux.org/packages/extra/any/edk2-ovmf/) for testing on EFI.

## Profile Structure
The profile structure is kept as simple as possible. You need this things for create profile:

 - airootfs directory 
 - airootfs customization file(s)
 - grub.cfg file
 - pacman.conf
 - packages file
 - profile.yaml [example](https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/blob/master/example-profile.yaml)

**Note:** You can look at profiles by this links: [TeaISO example profiles](https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/tree/master/profiles), [TeArch ISO profiles](https://gitlab.com/tearch-linux/configs/tearch-iso-profiles).