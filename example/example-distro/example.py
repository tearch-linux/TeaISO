import os, shutil, logging
from utils import execute_command, run_chroot, change_status

# This variables must be created. teaiso will replace with current working directory.
# airootfs_directory is rootfs and work_directory is working directory.
work_directory = None
airootfs_directory = None


def make_pkg_conf():
    # This function create rootfs with bootstrap script or configure package manager for instalation base package.
    change_status(work_directory, "system.make_pkg_conf")


def make_pkglist():
    # This function create installed package list
    change_status(work_directory, "system.make_pkglist")


def install_packages(cmd_line):
    # This function install package into rootfs
    change_status(work_directory, "system.install_packages")


def make_isowork():
    # This function prepare isowork directory for creating iso
    change_status(work_directory, "system.make_isowork")
