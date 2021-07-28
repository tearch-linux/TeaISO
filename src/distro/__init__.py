import os
from utils import run, inf, colorize, out
from colors import *
workdir=""
type="debian"
teaiso="/usr/lib/teaiso"

def set(option,variable):
    with open("{}/options.sh".format(workdir),"a") as f:
       f.write("{}={}\n".format(option,variable))
       out("{} : {}".format(colorize(option,green),variable))

def run_function(func):
    inf("=> Running: {}".format(colorize(func,0)))
    if 0 != run(" cd {1} ; bash -ec \"source {2}/distro/functions.sh ; source {2}/distro/{0}.sh; source {1}/options.sh ; {3}\"".format(type,workdir,teaiso,func)):
        exit (1)
    
def create_rootfs():
    run_function("create_rootfs")
    
def tools_init():
    run_function("tools_init")

def install_packages():
    run_function("install_packages")
    
def generate_isowork():
    run_function("generate_isowork")

def mount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        run("mount --bind /{0} /{1}/{0}".format(dir,rootfs))

def unmount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        while 0 == run("umount -lf -R /{}/{} 2>/dev/null".format(rootfs,dir)):
            True

def get_stage():
    if not os.path.exists("{}/stage".format(workdir)):
        set_stage(0)
        return 0
    with open("{}/stage".format(workdir),"r") as f:
        return int(f.read())
def set_stage(stage):
    with open("{}/stage".format(workdir),"w") as f:
        return f.write(str(stage))

