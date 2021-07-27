import os
from utils import out, err, colorize, run
from colors import *

output="/var/teaiso/output"
workdir="/var/teaiso/work"
profile="/usr/lib/teaiso/profiles/baseline"
debug=False
def show():
    out("{}\t: {}".format(colorize("Output directory",green),output))
    out("{}\t: {}".format(colorize("Working directory",green),workdir))
    out("{}\t: {}".format(colorize("Profile directory",green),profile))

def check():
    if not os.path.exists(output):
        os.makedirs(output)
    if os.path.exists(workdir):
        run("rm -rf {}".format(workdir))
    os.makedirs(workdir)
    if not os.path.exists(profile):
        err("Profile directory not exists:\n -> {}".format(profile))
