from utils import *
import sys, os
import settings
import common, distro
from help import help_message
nocheck=False

# argument parse
for i in sys.argv[1:]:
    if i.startswith("--"):
        i=i[2:]
        if i.startswith("output="):
            settings.output = get_argument_value(i,"output")
        elif i.startswith("workdir="):
            settings.workdir = get_argument_value(i,"workdir")
        elif i.startswith("profile="):
            settings.profile = get_argument_value(i,"profile")
    if i == "debug":
        settings.debug=True
    elif i == "nocolor": 
        disable_color()
    elif i == "simulate":
        warn("Simulation mode enabled.")
        set_simulation()
    elif i == "nocheck":
        nocheck = True
    elif i == "help":
        help_message()

if os.path.exists("./Makefile") and os.path.exists("./mkteaiso"):
    settings.teaiso = os.getcwd()+"/src"


sys.path.insert(0,settings.teaiso)


if not is_root():
    err("You must be root!")

os.environ.clear()
os.environ["PATH"]="/bin:/sbin:/usr/bin:/usr/sbin"

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
distro.set("workdir",settings.workdir)

# distro options
distro.set("name",common.get("name"))
distro.set("arch",common.get("arch"))
distro.set("distro",common.get("distro"))
distro.set("teaiso",settings.teaiso)
distro.set("profile",settings.profile)
distro.set("label",common.get("label"))
packages=common.get_package_list(common,settings)
distro.set("packages", "(" + ' '.join(packages) + ")")


# rootfs settings
settings.rootfs = settings.workdir+"/airootfs"
distro.set("rootfs",settings.rootfs)
distro.set("codename",common.get("codename","stable")) # for debian
distro.set("repository",common.get("repository")) # for debian
set_rootfs(settings.rootfs)

if settings.debug:
    dbg("Distro options:\n"+getoutput("cat "+settings.workdir+"/options.sh"))


# airootfs creation (stage 0)
if common.get_stage() <= 0:
    distro.tools_init()
    distro.create_rootfs()
    common.set_stage(0)
    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory_pre")):
        run("cp -prfv {}/* {}".format(settings.profile+"/"+common.get("airootfs_directory_pre"),settings.rootfs))
    os.chdir(settings.workdir)
    for i in common.get("customize_airootfs_pre",[]):
        run("chmod +x "+settings.profile+"/"+i)
        inf("==> Running: {}".format(colorize(i,0)))
        run(settings.profile+"/"+i)
    os.chdir(settings.teaiso)
else:
    inf("Using build stage: {}".format(colorize(distro.get_stage(),0)))    
common.mount_operations(settings.rootfs)

# install packages (stage 1)
if common.get_stage() < 1:
    distro.install_packages()
    common.set_stage(1)

# merge with airootfs directory (stage 2)
if common.get_stage() < 2:
    inf("Copy airootfs")
    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory")):
        run("cp -prfv {}/* {}".format(settings.profile+"/"+common.get("airootfs_directory"),settings.rootfs))
    common.set_stage(2)

# customize airootfs (stage 3)
if common.get_stage() < 3:
    inf("Customizing airootfs")
    os.chdir(settings.workdir)
    for i in common.get("customize_airootfs",[]):
        run("chmod +x "+settings.profile+"/"+i)
        inf("==> Running: {}".format(colorize(i,0)))
        run(settings.profile+"/"+i)
    os.chdir(settings.teaiso)
    common.set_stage(3)

common.unmount_operations(settings.rootfs)

if common.get_stage() < 4:
    distro.clear_rootfs()
    common.create_squashfs(settings)
    common.create_isowork(settings)
    distro.generate_isowork()
    common.set_stage(4)
common.create_iso(settings)
