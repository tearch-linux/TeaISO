import os
from utils import run, inf, colorize, out
from colors import *
workdir=""
type="debian"

def set(option,variable):
    with open("{}/options.sh".format(workdir),"a") as f:
       f.write("{}={}\n".format(option,variable))
       out("{} : {}".format(colorize(option,green),variable))

def run_function(func):
    inf("=> Running: {}".format(colorize(func,0)))
    if 0 != run("bash -ec \"source distro/functions.sh ; source distro/{}.sh; source {}/options.sh ; {}\"".format(type,workdir,func)):
        exit (1)
    
def create_rootfs():
    run_function("create_rootfs")

def mount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        run("mount --bind /{0} /{1}/{0}".format(dir,rootfs))

def unmount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        run("umount -lf -R /{}/{}".format(rootfs,dir))
