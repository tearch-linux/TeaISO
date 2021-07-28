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
    elif i == "debug":
        settings.debug=True
    elif i == "nocolor": 
        disable_color()
    elif i == "simulate":
        warn("Simulation mode enabled.")
        set_simulation()

if os.path.exists("../Makefile") and os.path.exists("../mkteaiso"):
    settings.teaiso = os.getcwd()

os.chdir(settings.teaiso)
settings.check()
settings.show()


# load profile
inf("Loading profile: "+ settings.profile+"/profile.yaml")
common.profile=common.parse_profile(settings.profile+"/profile.yaml")

# distro settings
distro.workdir = settings.workdir
distro.type=common.get("distro")
inf("Creating workdir for: "+distro.type)

if settings.debug:
    dbg("Profile content:\n"+str(common.profile))

# distro options
distro.set("arch",common.get("arch"))
distro.set("distro",common.get("distro"))
distro.set("teaiso",settings.teaiso)
distro.teaiso=settings.teaiso
packages=common.get_package_list(common,settings)
distro.set("packages", "(" + ' '.join(packages) + ")")


# rootfs settings
distro.set("rootfs",distro.workdir+"/airootfs")
distro.set("codename",common.get("codename","stable")) # for debian
distro.set("repository",common.get("repository")) # for debian
set_rootfs(distro.workdir+"/airootfs")

if settings.debug:
    dbg("Distro options:\n"+getoutput("cat "+distro.workdir+"/options.sh"))

distro.tools_init()
distro.create_rootfs()
