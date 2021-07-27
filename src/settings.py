from utils import out, colorize
from colors import *
output="/var/teaiso/output"
workdir="/var/teaiso/work"
profile="/usr/lib/teaiso/profile/baseline"
def show():
    out("{}\t: {}".format(colorize("Output directory",green),output))
    out("{}\t: {}".format(colorize("Working directory",green),workdir))
    out("{}\t: {}".format(colorize("Profile directory",green),profile))
    
