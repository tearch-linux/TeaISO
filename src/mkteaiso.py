from utils import *
import sys, os
import settings
import common, distro
nocheck=False
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
    elif i == "nocheck":
        nocheck = True

if os.path.exists("../Makefile") and os.path.exists("../mkteaiso"):
    settings.teaiso = os.getcwd()

os.chdir(settings.teaiso)
if not nocheck:
    settings.check()
else:
    warn("Settings checking skipped")
settings.show()


# load profile
settings.profile = getoutput("realpath "+settings.profile)
inf("Loading profile: "+ settings.profile+"/profile.yaml")
common.profile=common.parse_profile(settings.profile+"/profile.yaml")
if common.profile == None:
    err("Cannot load profile: profile.yaml is not valid")

if settings.debug:
    dbg("Profile content:\n"+str(common.profile))
    
# distro settings
distro.workdir = settings.workdir
distro.type=common.get("distro")

# distro options
distro.set("arch",common.get("arch"))
distro.set("distro",common.get("distro"))
distro.set("teaiso",settings.teaiso)
distro.set("profile",settings.profile)
distro.teaiso=settings.teaiso
packages=common.get_package_list(common,settings)
distro.set("packages", "(" + ' '.join(packages) + ")")


# rootfs settings
settings.rootfs = distro.workdir+"/airootfs"
distro.set("rootfs",settings.rootfs)
distro.set("codename",common.get("codename","stable")) # for debian
distro.set("repository",common.get("repository")) # for debian
set_rootfs(settings.rootfs)

if settings.debug:
    dbg("Distro options:\n"+getoutput("cat "+distro.workdir+"/options.sh"))

# airootfs creation (stage 0)
distro.tools_init()
if distro.get_stage() <= 0:
    distro.create_rootfs()
    distro.set_stage(0)
    
distro.mount_operations(settings.rootfs)

# install packages (stage 1)
if distro.get_stage() < 1:
    distro.install_packages()
    distro.set_stage(1)

# merge with airootfs directory (stage 2)
if distro.get_stage() < 2:
    inf("Copy airootfs")
    run("cp -prfv {} {}".format(settings.profile+"/airootfs",settings.rootfs))
    distro.set_stage(2)

# customize airootfs (stage 3)
if distro.get_stage() < 3:
    inf("Customizing airootfs")
    os.chdir(settings.workdir)
    for i in common.get("customize_airootfs",[]):
        run("chmod +x "+settings.profile+"/"+i)
        inf("==> Running: {}".format(colorize(i,0)))
        run(settings.profile+"/"+i)
    os.chdir(settings.teaiso)
    distro.set_stage(3)

distro.unmount_operations(settings.rootfs)
