import os, shutil, logging
from utils import execute_command, run_chroot, change_status

work_directory = None
airootfs_directory = None


def make_pkg_conf():
    airootfs_directory = work_directory + '/' + iso_profile["arch"]

    if os.path.exists(airootfs_directory + '/etc/shadow'):
        return
    execute_command('debootstrap --no-merged-usr stable ' + airootfs_directory)

    logging.info("apt.conf generated successfully!")
    change_status(work_directory, "system.make_pkg_conf")


def make_pkglist():
    run_chroot(work_directory, iso_profile, "apt list --installed ", work_directory + "/" + "packages.list")

    logging.info("Pkglist generated!")
    change_status(work_directory, "system.make_pkglist")


def install_packages(cmd_line):
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    packages = ' '.join(iso_profile["packages"])

    if cmd_line.verbose:
        command = "chroot {} apt install {}".format(airootfs_directory, packages)
    else:
        command = "chroot {} apt install -yq {}".format(airootfs_directory, packages)

    execute_command(command)

    logging.info("Packages installed to airootfs!")
    change_status(work_directory, "system.install_packages")


def make_isowork(cmd_line, compression_tool="squashfs"):
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    execute_command("du -sb {} | cut -f1 > {}/isowork/live/filesystem.size".format(airootfs_directory, work_directory))

    shutil.copyfile(iso_profile["grub_cfg"], work_directory + "/isowork/boot/grub/grub.cfg")
    if os.path.exists("{0}/live/airootfs.sfs".format(work_directory + "/isowork/")):
        execute_command("mv {0}/live/airootfs.sfs {0}/live/filesystem.squashfs".format(work_directory + "/isowork/"))
    execute_command(
        "md5sum {0}/live/filesystem.squashfs > {0}/live/filesystem.md5sum".format(work_directory + "/isowork/"))
    shutil.copy(work_directory + "/" + "packages.list", work_directory + "/isowork")

    logging.info("Isowork generated!")
    change_status(work_directory, "system.make_isowork")
