#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# TeaISO - ISO generation tool for Arch Linux.
# License: GPL-3

# TODO: Fix hooks for Ventoy.
# TODO: Add arch-outside pacstrap
import argparse
import os
import sys
import shutil
import yaml
import time
import logging
from datetime import date, datetime
from collections import OrderedDict

#portable and normal mode 
if os.path.exists("../Makefile"):
   sys.path.insert(0, "../distro")
else:
    sys.path.insert(0, "/usr/lib/teaiso")
    sys.path.insert(0, "/usr/lib/teaiso/distro")
    
from utils import execute_command, run_chroot, remove_all_contents, change_status, check_status, mount_operations

if os.getuid() != 0:
    logging.error("You need to have root privileges to run this script!")
    sys.exit(1)
print(os.getuid())
VERSION = "1.1.2"
compression_options = "-comp gzip"

logging.basicConfig(handlers=[logging.FileHandler("/var/log/teaiso.log"), logging.StreamHandler()],
                    format='%(asctime)s [mkteaiso] %(levelname)s: %(message)s', datefmt='%d/%m/%y %H:%M:%S')


# Argument Parser
def arguments():
    description = "ISO generation tool for Arch Linux and Debian, v{0}".format(VERSION)
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-o", "--output",
        help="Output directory of ISO.",
    )
    parser.add_argument(
        "-w", "--work",
        help="Work directory of ISOs preparation files.",
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Enable detailed verbose output.",
        action="store_true")
    parser.add_argument(
        "-c", "--clean",
        help="Clean work directory after the ISO generation.",
        action="store_true")
    parser.add_argument(
        "-p", "--profile",
        help="Profile directory for ISO.",
        required=True
    )
    return parser.parse_args()


def validate_profile(contents):
    required_keys = ['name', 'publisher', 'label', 'application_id', 'airootfs_directory', 'arch', 'pacman', 'grub_cfg',
                     'packages', 'distro']

    # Check required keys
    for key in required_keys:
        if key not in contents:
            logging.error('\'{}\' not found in profile.yaml. Please check your profile!'.format(key))
            sys.exit(1)

    logging.info('Profile validated successfully!')


# Read profile arguments
def read_profile(directory_original):
    global compression_options
    logging.info('Reading profile...')

    directory = os.path.realpath(directory_original) + "/"
    file_name = directory + "profile.yaml"

    if os.path.exists(file_name):
        file = open(file_name).read()

        contents = yaml.load(file, Loader=yaml.FullLoader)
        validate_profile(contents)

        contents["airootfs_directory"] = directory + contents["airootfs_directory"]
        contents["pacman"] = contents["pacman"]
        contents["grub_cfg"] = directory + contents["grub_cfg"]

        packages = []
        for package in contents["packages"]:
            package_names = open(directory + package).read().split("\n")
            [packages.append(str(p)) for p in package_names if not (p.startswith('#'))]
        contents["packages"] = list(OrderedDict.fromkeys(packages))

        if 'file_permissions' in contents:
            file_permissions = {}
            for file in contents["file_permissions"]:
                file = file.split("|")
                file_permissions[file[0]] = file[1]
            contents["file_permissions"] = file_permissions

        if 'customize_airootfs' in contents:
            customize_airootfs = {}
            for source in contents["customize_airootfs"]:
                if os.path.exists(directory + source):
                    customize_airootfs[os.path.basename(source)] = directory + source
                else:
                    logging.error("{} doesn't exists!".format(directory + source))
                    sys.exit(1)
            contents["customize_airootfs"] = customize_airootfs

        if 'compression_options' in contents:
            compression_options = contents['compression_options']
            del contents['compression_options']
        else:
            logging.warning(
                'Compression options not found! Using \'{}\' as default!'.format(compression_options))

        if contents['distro'] == 'archlinux':
            contents['pacman'] = directory + contents["pacman"]
        else:
            contents['pacman'] = None

        logging.info('Done!')

        return contents
    else:
        logging.error('profile.yaml doesn\'t exists in {} directory!'.format(directory))
        sys.exit(1)


def create_directories():
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
        logging.info("Work directory created!")
    else:
        logging.info("Work directory already exists!")

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
        logging.info("Output directory created!")
    else:
        logging.info("Output directory already exists!")

    change_status(work_directory, "create_directories")


def make_custom_airootfs():
    execute_command("mkdir -p \"{}\"".format(target))
    execute_command(
        "cp -prf --no-preserve=ownership \"{}\"/* \"{}\"/".format(iso_profile["airootfs_directory"], target))

    os.chmod(target + '/etc/shadow', 0o400) if os.path.exists(target + '/etc/shadow') else None
    os.chmod(target + '/etc/gshadow', 0o400) if os.path.exists(target + '/etc/gshadow') else None

    # Set permissions of home and root directories
    if os.path.exists(target + '/etc/passwd'):
        contents = open(target + '/etc/passwd', "r").read().rstrip().split(':')

        if contents[5].startswith('/') or contents[5] is None:
            if os.path.exists(target + contents[5]):
                execute_command("chown -hR -- {}:{} {}".format(contents[2], contents[3], target + contents[5]))
                execute_command("chmod -f 0750 -- {}".format(target + contents[5]))
            else:
                execute_command(
                    "install -d -m 0750 -o {} -g {} -- {}".format(contents[2], contents[3], target + contents[5]))

    logging.info("Custom airootfs generated successfully!")
    change_status(work_directory, "make_custom_airootfs")


def customize_airootfs():
    mount_operations(target, "mount")

    if 'customize_airootfs' in iso_profile:
        root_directory = target + "/root/customize/"
        execute_command("mkdir -p {}".format(root_directory + "customize"))

        for source, file in iso_profile["customize_airootfs"].items():
            shutil.copyfile(file, root_directory + source)
            os.chmod(root_directory + source, 0o755)

            run_chroot(work_directory, iso_profile, "/root/customize/" + source)
        logging.info("Airootfs customized!")
    else:
        logging.warning('Customize airootfs not found. Skipping!')

    change_status(work_directory, "customize_airootfs")


def set_permissions():
    mount_operations(target, "umount")

    if 'file_permissions' in iso_profile:
        for name, permission in iso_profile["file_permissions"].items():
            permission = permission.split(':')
            name = work_directory + '/' + iso_profile["arch"] + name

            execute_command("chown -fh -- {}:{} {}".format(permission[0], permission[1], name))
            execute_command("chmod -f -- {} {}".format(permission[2], name))
        logging.info("Permissions set!")
    else:
        logging.warning('File permissions not found. Skipping!')

    change_status(work_directory, "set_permissions")


def cleanup():
    # Copy boot files before, removing initramfs
    execute_command("mkdir -p {}".format(work_directory + "/isowork/boot/grub"))
    execute_command("mkdir -p {}".format(work_directory + "/isowork/live"))
    execute_command("cp -prf {}/* \"{}/\"".format(target + "/boot", work_directory + "/isowork/boot"))

    remove_all_contents(target + "/var/lib/pacman/sync/*")
    remove_all_contents(target + "/var/log/*")
    remove_all_contents(target + "/var/tmp/*")
    execute_command("find \"{}/var/lib/pacman\" -maxdepth 1 -type f -delete".format(target), False)
    execute_command("find \"{}/var/cache/apt/archives\" -maxdepth 1 -type f -delete".format(target), False)
    if os.path.exists(target + "/root/customize"):
        shutil.rmtree(target + "/root/customize")

    open(target + "/etc/machine-id", 'w+').close()

    logging.info("Airootfs cleaned!")
    change_status(work_directory, "cleanup")


def prepare_squashfs():
    mount_operations(target, "umount")
    execute_command(
        "mksquashfs \"{}\" {}/airootfs.sfs -wildcards {}".format(target, work_directory + "/isowork/live",
                                                                 compression_options))

    logging.info("Squashfs prepared!")
    change_status(work_directory, "prepare_squashfs")


def generate_iso():
    # Create Directories
    execute_command("mkdir -p {}/isowork/EFI/boot".format(work_directory))
    execute_command("mkdir -p {}/efiboot".format(work_directory))

    # Copy Necessary Directories
    execute_command("cp -r {}/usr/lib/grub/i386-pc/ {}/isowork/boot/grub/".format(target, work_directory), False)
    execute_command("cp -r {}/usr/lib/grub/i386-efi/ {}/isowork/boot/grub/".format(target, work_directory), False)
    execute_command("cp -r {}/usr/lib/grub/x86_64-efi/ {}/isowork/boot/grub/".format(target, work_directory), False)
    execute_command("cp -r {}/usr/share/grub/themes/ {}/isowork/boot/grub/".format(target, work_directory), False)

    # Generate Bootloaders
    execute_command(
        "grub-mkimage -d {0}/isowork/boot/grub/i386-pc/ -o {0}/isowork/boot/grub/i386-pc/core.img -O i386-pc -p /boot/grub biosdisk iso9660".format(
            work_directory), False)
    execute_command(
        "cat {0}/isowork/boot/grub/i386-pc/cdboot.img {0}/isowork/boot/grub/i386-pc/core.img > {0}/isowork/boot/grub/i386-pc/eltorito.img".format(
            work_directory), False)
    execute_command(
        "grub-mkimage -d {0}/isowork/boot/grub/x86_64-efi/ -o {0}/isowork/EFI/boot/bootx64.efi -O x86_64-efi -p /boot/grub iso9660".format(
            work_directory), False)
    execute_command(
        "grub-mkimage -d {0}/isowork/boot/grub/i386-efi/ -o {0}/isowork/EFI/boot/bootia32.efi -O i386-efi -p /boot/grub iso9660".format(
            work_directory), False)

    # Generate efi.img
    execute_command("truncate -s 4M {}/isowork/efi.img".format(work_directory))
    execute_command("mkfs.fat -n TEAISO_EFI {}/isowork/efi.img &>/dev/null".format(work_directory))
    execute_command("mount -o loop {0}/isowork/efi.img {0}/efiboot".format(work_directory))
    execute_command("mkdir -p {}/efiboot/EFI/boot".format(work_directory))
    execute_command(
        "grub-mkimage -d {0}/isowork/boot/grub/x86_64-efi/ -o {0}/efiboot/EFI/boot/bootx64.efi -O x86_64-efi -p /boot/grub iso9660".format(
            work_directory), False)
    execute_command(
        "grub-mkimage -d {0}/isowork/boot/grub/i386-efi/ -o {0}/efiboot/EFI/boot/bootia32.efi -O i386-efi -p /boot/grub iso9660".format(
            work_directory), False)
    execute_command("umount -fl {}/efiboot".format(work_directory))

    # Miscellaneous
    execute_command("grub-editenv {}/isowork/boot/grub/grubenv set menu_show_once=1".format(work_directory))

    # Xorriso
    modification_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-00").replace("-", "")

    execute_command("""xorriso -as mkisofs \
                --modification-date={0} \
                --protective-msdos-label \
                -volid "{1}" \
                -appid "{2}" \
                -publisher "{3}" \
                -preparer "Prepared by TeaISO v{4}" \
                -r -graft-points -no-pad \
                --sort-weight 0 / \
                --sort-weight 1 /boot \
                --grub2-mbr {5}/isowork/boot/grub/i386-pc/boot_hybrid.img \
                -iso_mbr_part_type 0x00 \
                -partition_offset 16 \
                -b boot/grub/i386-pc/eltorito.img \
                -c boot.catalog \
                -no-emul-boot -boot-load-size 4 -boot-info-table --grub2-boot-info \
                -eltorito-alt-boot \
                -append_partition 2 0xef {5}/isowork/efi.img \
                -e --interval:appended_partition_2:all:: \
                -no-emul-boot \
                -full-iso9660-filenames \
                -iso-level 3 -rock -joliet \
                -o {6} \
                {5}/isowork/""".format(modification_date, iso_profile["label"], iso_profile["application_id"],
                                       iso_profile["publisher"], VERSION, work_directory,
                                       output_directory + "/" + iso_name))

    logging.info("ISO generated!")
    change_status(work_directory, "generate_iso")


def show_verbose_profile():
    today = date.today()
    iso_name = iso_profile["name"] + "-" + today.strftime("%d-%m-%Y") + "-" + iso_profile["arch"] + ".iso"

    logging.info("mkteaiso configuration settings:")
    logging.info("                  Profile:   {}".format(iso_profile["name"]))
    logging.info("                    Label:   {}".format(iso_profile["label"]))
    logging.info("           Application ID:   {}".format(iso_profile["application_id"]))
    logging.info("            ISO publisher:   {}".format(iso_profile["publisher"]))
    logging.info("            ISO file name:   {}".format(iso_name))
    logging.info("       Airootfs directory:   {}".format(iso_profile["airootfs_directory"]))
    logging.info("        Working directory:   {}".format(work_directory))
    logging.info("         Output directory:   {}".format(output_directory))
    logging.info("Pacman configuration file:   {}".format(iso_profile["pacman"]))
    logging.info("             Architecture:   {} ".format(iso_profile["arch"]))
    logging.info("               Build date:   {}".format(time.time()))
    logging.info("         File permissions:   {}".format(
        iso_profile["file_permissions"] if 'file_permissions' in iso_profile else 'N/A'))
    logging.info("       Customize Airootfs:   {}".format(
        iso_profile["customize_airootfs"] if 'customize_airootfs' in iso_profile else 'N/A'))
    logging.info("                 Packages:   {}".format(iso_profile["packages"]))
    logging.info("      Compression Options:   '{}'\n".format(compression_options))


if __name__ == "__main__":

    cmd_line = arguments()
    # Clean env varibles
    os.environ.clear()

    # Set directories
    output_directory = os.path.realpath(cmd_line.output or 'output')
    work_directory = os.path.realpath(cmd_line.work or 'work')

    iso_profile = read_profile(cmd_line.profile)
    iso_name = iso_profile["name"] + "-" + date.today().strftime("%d-%m-%Y") + "-" + iso_profile["arch"] + ".iso"
    target = os.path.realpath(work_directory + "/" + iso_profile["arch"])

    if iso_profile["distro"] == 'debian':
        import debian as system
    elif iso_profile["distro"] == 'archlinux':
        import archlinux as system
    else:
        logging.error("Unsupported distro type detected")
        sys.exit(1)

    # Umount if already mounted. (for easy use rm -rf work output)
    mount_operations(target, "umount")

    if cmd_line.verbose:
        logging.getLogger().setLevel(logging.INFO)
        show_verbose_profile()

    system.work_directory = work_directory
    system.iso_profile = iso_profile

    # Prepare & Generate ISO
    steps = ["create_directories()", "system.make_pkg_conf()", "make_custom_airootfs()",
             "system.install_packages(cmd_line)", "customize_airootfs()", "system.make_pkglist()", "set_permissions()",
             "cleanup()", "prepare_squashfs()", "system.make_isowork()"]

    for step in steps:
        if check_status(work_directory, step.split('(')[0]):
            eval(step)

    if check_status(work_directory, "generate_iso"):
        generate_iso()

        if cmd_line.clean:
            execute_command("rm -rf {}".format(work_directory))
    else:
        logging.error('ISO already created! If you want re-create ISO, you should remove work and output directories!')
        sys.exit(1)
