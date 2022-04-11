import os
from utils import run, inf, colorize, out
from colors import *


def set(option, variable):
    if not variable:
        return
    workdir = os.environ["workdir"]
    with open("{}/options.sh".format(workdir), "a") as f:
        if type(variable) == type(""):
            f.write("{}='{}'\n".format(option, variable))
        elif type(variable) == type([]):
            variable = " ".join(variable)
            f.write("{}=({})\n".format(option, variable))
        else:
            f.write("{}={}\n".format(option, variable))
    os.environ[option] = variable
    #out("{} : {}".format(colorize(option, green), variable))


def get(option, default=""):
    if option in os.environ:
        return os.environ[option]
    return default


def run_function(func):
    inf("=> Running: {}".format(colorize(func, 0)))
    if 0 != run(" cd {1} ; bash -ec \"source {2}/distro/functions.sh ; source {2}/distro/{0}.sh; source {1}/options.sh ; {3}\"".format(get("distro"), get("workdir"), get("teaiso"), func)):
        exit(1)


def create_rootfs():
    run_function("create_rootfs")


def populate_rootfs():
    run_function("populate_rootfs")


def tools_init():
    run_function("tools_init")


def install_packages():
    run_function("install_packages")


def make_pkglist():
    run_function("make_pkglist")


def customize_airootfs():
    run_function("customize_airootfs")


def clear_rootfs():
    run_function("clear_rootfs")


def generate_isowork():
    run_function("generate_isowork")
