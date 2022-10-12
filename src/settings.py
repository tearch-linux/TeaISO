import os, platform
import time
from utils import out, err, inf, colorize, run
from colors import *

output = "/var/lib/teaiso/output"
workdir = "/var/lib/teaiso/work/{}".format(int(time.time()*1000))
teaiso = "/usr/lib/teaiso"
profile = "archlinux"
shared = None
compression = []
rootfs = None
iso_merge = None
debug = False
interactive = False

def show(contents, packages):
    inf("mkteaiso configuration settings:")

    inf("\t{}: {}".format(colorize("Profile Directory", bold), profile))
    inf("\t{}: {}".format(colorize("Working Directory", bold), workdir))
    inf("\t{}: {}".format(colorize("Output Directory", bold), output))
    inf("\t{}: {}".format(colorize("Shared Directory", bold), shared))

    inf("\t{}: {}".format(colorize("Profile", bold), contents["name"]))
    inf("\t{}: {}".format(colorize("Label", bold), contents["label"]))
    inf("\t{}: {}".format(colorize("Application ID", bold),
        contents["application_id"]))
    inf("\t{}: {}".format(
        colorize("ISO publisher", bold), contents["publisher"]))
    inf("\t{}: {}".format(colorize("Architecture", bold), platform.uname().machine))
    inf("\t{}: {}".format(colorize("Packages", bold), packages))
    inf("\t{}: {}".format(colorize("Build date", bold), time.time()))
    inf("\t{}: {}".format(colorize("ISO name", bold), contents["iso_name"]))
    inf("\t{}: {}".format(colorize("File permissions", bold),
        contents["airootfs_directory"] if 'airootfs_directory' in contents else 'N/A'))
    inf("\t{}: {}".format(colorize("Airootfs directory", bold),
        contents["file_permissions"] if 'file_permissions' in contents else 'N/A'))
    inf("\t{}: {}".format(colorize("Customize airootfs", bold),
        contents["customize_airootfs"] if 'customize_airootfs' in contents else 'N/A'))
    inf("\t{}: {}".format(
        colorize("Compression options", bold), contents["compression"]))

    if contents["distro"] == "archlinux" or contents["distro"] == "tearch":
        inf("\t{}: {}".format(colorize("Pacman Configuration", bold),
            os.path.realpath(profile + "/" + contents["pacman"]) if 'pacman' in contents else 'N/A'))
    elif contents["distro"] == "debian" or contents["distro"] == "ubuntu":
        inf("\t{}: {}".format(colorize("Codename", bold),
            contents["codename"] if 'codename' in contents else 'N/A'))
        inf("\t{}: {}".format(colorize("Variant", bold),
            contents["variant"] if 'variant' in contents else 'N/A'))
        inf("\t{}: {}".format(colorize("Repository", bold),
            contents["repository"] if 'repository' in contents else 'N/A'))
    inf("\t{}: {}".format(colorize("Kernel cmdline", bold),
        contents["linux_args"] if 'linux_args' in contents else 'N/A'))
    if interactive == "true":
        if input("Do you wanna continue? [Y/n]").lower()[0] != "y": 
            exit(1)

def check():
    if not os.path.exists(output):
        os.makedirs(output)
    if os.path.exists(workdir):
        inf("Clearing old work directory")
        os.system("rm -rf {}".format(workdir))
    os.makedirs(workdir)
    if not os.path.exists(profile) and not os.path.exists(teaiso+"/profiles/"+profile):
        err("Profile directory not exists:\n -> {}".format(profile))
