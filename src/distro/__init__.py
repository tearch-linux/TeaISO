import os
from utils import run
workdir=""
type="debian"

def set(option,variable):
    with open("{}/options.sh".format(workdir),"w") as f:
       f.write("{}={}".format(option,variable))

def run_function(func):
    run("bash -exc \"source distro/{}.sh; source {}/options.sh ; {}\"".format(type,workdir,func))
    
def create_rootfs():
    run_function("create_rootfs")
