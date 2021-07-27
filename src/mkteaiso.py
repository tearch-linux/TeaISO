from utils import *
import sys, os
import settings
import common, distro

if not is_root():
    err("You must be root!")

# argument parse
for i in sys.argv:
    if i.startswith("--"):
        i=i[2:]
    if i.startswith("output="):
        settings.output = get_argument_value(i,"output")
    elif i.startswith("workdir="):
        settings.workdir = get_argument_value(i,"workdir")
    elif i.startswith("profile="):
        settings.profile = get_argument_value(i,"profile")

settings.check()
settings.show()

# load profile
common.profile=common.parse_profile(settings.profile+"/profile.yaml")

# distro settings
distro.workdir = settings.workdir
print(common.profile)
distro.type=common.get("distro")

distro.set("arch",common.get("arch"))

for file in common.get("packages"):
    file = settings.profile + "/" + file
    
    if not os.path.exists(file):
        inf("Packages file not exists:\n -> {}".format(file))
    
    packages = []
    with open(file, "r") as f:
        for line in f.read().split("\n"):
            if not line.startswith("#"):
                packages.append(line.strip())
distro.set("packages", "(" + ' '.join(packages) + ")")

distro.create_rootfs()
