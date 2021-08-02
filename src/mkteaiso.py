from utils import *
import sys
import os
import settings
import common
import distro
from help import help_message
nocheck = False
os.umask(18) # set umask as 022
# argument parse


for i in sys.argv[1:]:
    if common.is_arg(i,"output"):
        settings.output = common.get_value(i)
    elif common.is_arg(i,"work"):
        settings.workdir = common.get_value(i)
    elif common.is_arg(i,"profile"):
        settings.profile =common.get_value(i)
        
    elif common.is_arg(i,"debug"):
        settings.debug = True
    elif i == "--nocolor":
        disable_color()
    elif i == "--simulate":
        warn("Simulation mode enabled.")
        set_simulation()
    elif i == "--nocheck":
        nocheck = True
    elif common.is_arg(i,"help"):
        help_message()

if os.path.exists("./Makefile") and os.path.exists("./mkteaiso"):
    settings.teaiso = os.getcwd()+"/src"


sys.path.insert(0, settings.teaiso)


if not is_root():
    err("You must be root!")

os.environ.clear()
os.environ["PATH"] = "/bin:/sbin:/usr/bin:/usr/sbin"

if not nocheck:
    settings.check()
else:
    warn("Settings checking skipped")
settings.show()


# load profile
settings.profile = getoutput("realpath "+settings.profile)
inf("Loading profile: " + settings.profile+"/profile.yaml")
common.profile = common.parse_profile(settings.profile+"/profile.yaml")
if common.profile == None:
    err("Cannot load profile: profile.yaml is not valid")

if settings.debug:
    dbg("Profile content:\n"+str(common.profile))

# distro settings
distro.set("workdir", settings.workdir)

# distro options
packages = common.get_package_list(common, settings)

distro.set("name", common.get("name"))
distro.set("arch", common.get("arch"))
distro.set("distro", common.get("distro"))
distro.set("label", common.get("label"))
distro.set("teaiso", settings.teaiso)
distro.set("profile", settings.profile)
distro.set("packages", "(" + ' '.join(packages) + ")")


# rootfs settings
settings.rootfs = settings.workdir+"/airootfs"

distro.set("rootfs", settings.rootfs)
distro.set("workdir", settings.workdir)
distro.set("codename", common.get("codename", "stable"))  # for debian
distro.set("repository", common.get("repository"))  # for debian
set_rootfs(settings.rootfs)

if settings.debug:
    dbg("Distro options:\n"+getoutput("cat "+settings.workdir+"/options.sh"))


# airootfs creation (stage 0)
if common.get_stage() <= 0:
    distro.tools_init()
    distro.create_rootfs()
    common.set_stage(0)

    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory_pre")) and len(common.get("airootfs_directory_pre")) > 0:
        run("cp -af --no-preserve=ownership,mode \"{}\"/* \"{}\"/".format(settings.profile+"/" + common.get("airootfs_directory_pre"), settings.rootfs))

    os.chdir(settings.workdir)
    for i in common.get("customize_airootfs_pre", []):
        os.chmod(settings.profile + "/" + i, 0o755)
        inf("==> Running: {}".format(colorize(i, 0)))
        run(settings.profile+"/"+i)
    os.chdir(settings.teaiso)
else:
    inf("Using build stage: {}".format(colorize(distro.get_stage(), 0)))

common.mount_operations(settings.rootfs)

# install packages (stage 1)
if common.get_stage() < 1:
    distro.install_packages()
    common.set_stage(1)

# merge with airootfs directory (stage 2)
if common.get_stage() < 2:
    inf("Copy airootfs")
    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory")) and len(common.get("airootfs_directory")) > 0:
                run("cp -af --no-preserve=ownership,mode \"{}\"/* \"{}\"/".format(settings.profile +"/" + common.get("airootfs_directory"), settings.rootfs))
        
    os.chmod(settings.rootfs + '/etc/shadow',
             0o400) if os.path.exists(settings.rootfs + '/etc/shadow') else None
    os.chmod(settings.rootfs + '/etc/gshadow',
             0o400) if os.path.exists(settings.rootfs + '/etc/gshadow') else None

    # Set permissions of home and root directories if exists
    if os.path.exists(settings.rootfs + '/etc/passwd'):
        contents=open(settings.rootfs + '/etc/passwd',
                      "r").read().rstrip().split(':')

        if contents[5].startswith('/') or contents[5] is None:
            if os.path.exists(settings.rootfs + contents[5]):
                run(
                    "chown -hR -- {}:{} {}".format(contents[2], contents[3], settings.rootfs + contents[5]))
                run(
                    "chmod -f 0750 -- {}".format(settings.rootfs + contents[5]))
            else:
                run(
                    "install -d -m 0750 -o {} -g {} -- {}".format(contents[2], contents[3], settings.rootfs + contents[5]))
                
    common.set_stage(2)

# customize airootfs (stage 3)
if common.get_stage() < 3:
    inf("Customizing airootfs")
    os.chdir(settings.workdir)
    for i in common.get("customize_airootfs", []):
        os.chmod(settings.profile + "/" + i, 0o755)
        inf("==> Running: {}".format(colorize(i, 0)))
        run(settings.profile+"/"+i)
    os.chdir(settings.teaiso)
    common.set_stage(3)
    
# Make package list (stage 4)
if common.get_stage() < 4:
    distro.make_pkglist()
    common.set_stage(4)
    
common.unmount_operations(settings.rootfs)

# Set permissions if exists (stage 5) 
if common.get_stage() < 5:
    if 'file_permissions' in common.profile:
        for name, permission in common.profile["file_permissions"].items():
            permission = permission.split(':')

            run("chown -fh -- {}:{} {}".format(permission[0], permission[1], settings.rootfs + "/" + name))
            run("chmod -f -- {} {}".format(permission[2], settings.rootfs + "/" + name))
        inf("Permissions set!")

    common.set_stage(5)

# Generate ISO (stage 6)
if common.get_stage() < 6:
    distro.clear_rootfs()
    common.create_squashfs(settings)
    common.create_isowork(settings)
    distro.generate_isowork()
    common.set_stage(6)
common.create_iso(settings)
