from utils import *
import sys
import settings

# argument parse
for i in sys.argv:
    if i.startswith("--"):
        i=i[2:]
    if i.startswith("output="):
        settings.output = get_argument_value(i,"output")
    elif i.startswith("workdir="):
        settings.workdir = get_argument_value(i,"workdir")
settings.show()

# rootfs settings
set_rootfs("/var/debian")
run("chroot||cat /etc/os-release")
