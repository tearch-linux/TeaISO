import os
from utils import out, err, inf, colorize, run
from colors import *

output="/var/teaiso/output"
workdir="/var/teaiso/work"
teaiso="/usr/lib/teaiso"
profile="profiles/baseline"
rootfs=None
debug=False
def show():
    out("{}\t: {}".format(colorize("Output directory",green),output))
    out("{}\t: {}".format(colorize("Working directory",green),workdir))
    out("{}\t: {}".format(colorize("Profile directory",green),profile))

def check():
    if not os.path.exists(output):
        os.makedirs(output)
    if os.path.exists(workdir):
        inf("Clearing old work directory")
        os.system("rm -rfv {}".format(workdir))
    os.makedirs(workdir)
    if not os.path.exists(profile) and not os.path.exists(teaiso+"/profiles/"+profile):
        err("Profile directory not exists:\n -> {}".format(profile))
