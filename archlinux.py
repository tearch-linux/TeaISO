import os, shutil, logging
from utils import execute_command, run_chroot, change_status

work_directory = None
airootfs_directory = None


def make_pkg_conf():
    target_pacman_conf = os.path.realpath(work_directory + "/pacman.conf")
    shutil.copyfile(iso_profile["pacman"], target_pacman_conf)

    os.chmod(target_pacman_conf, 0o775)

    logging.info("pacman.conf generated successfully!")
    change_status(work_directory, "system.make_pkg_conf")


def make_pkglist():
    run_chroot(work_directory, iso_profile, "pacman -Qqn", work_directory + "/packages.list")

    logging.info("Pkglist generated!")
    change_status(work_directory, "system.make_pkglist")


def install_packages(cmd_line):
    pacman_conf_directory = work_directory + '/' + "pacman.conf"
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    packages = ' '.join(iso_profile["packages"])

    if cmd_line.verbose:
        command = "pacstrap -C {} -c -i -G -M -- {} {}".format(pacman_conf_directory, airootfs_directory, packages)
    else:
        command = "pacstrap -C {} -c -G -M -- {} {} &> /dev/null".format(pacman_conf_directory, airootfs_directory,
                                                                         packages)
    execute_command(command)

    logging.info("Packages installed to airootfs!")
    change_status(work_directory, "system.install_packages")


def make_isowork():
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    execute_command("du -sb {} | cut -f1 > {}/isowork/live/airootfs.size".format(airootfs_directory, work_directory))

    shutil.copyfile(iso_profile["grub_cfg"], work_directory + "/isowork/boot/grub/grub.cfg")

    execute_command("md5sum {0}/live/airootfs.sfs > {0}/live/airootfs.md5sum".format(work_directory + "/isowork/"))
    shutil.copy(work_directory + "/packages.list", work_directory + "/isowork")

    logging.info("Isowork generated!")
    change_status(work_directory, "system.make_isowork")
