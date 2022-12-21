from utils import *
import sys
import os, platform
import settings
import common
import distro

nocheck = False
create_profile = False
gpg_key = None
interactive = "false"

os.umask(18)  # set umask as 022

# argument parse
for i in sys.argv[1:]:
    if Args.is_arg(i, "output"):
        settings.output = os.path.realpath(Args().get_value(i))
    elif Args.is_arg(i, "work"):
        settings.workdir = os.path.realpath(Args().get_value(i))
    elif Args.is_arg(i, "profile"):
        settings.profile = os.path.realpath(Args().get_value(i))
    elif Args.is_arg(i, "shared"):
        settings.shared = os.path.realpath(Args().get_value(i))
    elif Args.is_arg(i, "create"):
        create_profile = Args().get_value(i)
    elif Args.is_arg(i, "gpg"):
        gpg_key = Args().get_value(i)
    elif Args.is_arg(i, "debug"):
        settings.debug = True
    elif i == "--nocolor" or "NO_COLOR" in os.environ:
        disable_color()
    elif i == "--simulate":
        warn("Simulation mode enabled.")
        set_simulation()
    elif i == "--nocheck":
        nocheck = True
    elif i == "--interactive":
        interactive = "true"
    elif i == "--version":
        out("mkteaiso (ISO generation tool for GNU/Linux), v{}".format(VERSION))
    elif Args.is_arg(i, "help"):
        Args.help_message()

if os.path.exists("./Makefile") and os.path.exists("./mkteaiso"):
    settings.teaiso = os.getcwd()+"/src"

sys.path.insert(0, settings.teaiso)

# load profile
run("python3 \"{}/misc/check-command.py\"".format(settings.teaiso))


if create_profile:
    run("cp -rf {0}/profiles/{1} {2}/{1}".format(settings.teaiso,
        create_profile, os.getcwd()))
    exit(0)

if not is_root():
    err("You must be root!")

if interactive != "true":
    try:
        os.close(0)
    except:
        warn("Failed to close stdin")
        pass
settings.interactive = interactive

# Disable selinux
os.system("setenforce 0 &>/dev/null")

os.environ.clear()
os.environ["PATH"] = "/bin:/sbin:/usr/bin:/usr/sbin"
os.environ["DEBIAN_FRONTEND"] = "noninteractive"

if os.path.exists(settings.teaiso+"/profiles/"+settings.profile):
    settings.profile = settings.teaiso+"/profiles/"+settings.profile
settings.profile = os.path.realpath(settings.profile)


# rootfs settings
settings.rootfs = settings.workdir+"/airootfs"
set_rootfs(settings.rootfs)
Mount.unmount(settings.rootfs)


if not nocheck:
    settings.check()
else:
    warn("Settings checking skipped")


# load profile
if os.path.exists(settings.profile+"/profiledef.sh"):
    run("cd \"{}\" ; bash -ec \"{}/misc/import_profiledef.sh\" > \"{}\"".format(
        settings.profile, settings.teaiso, settings.profile+"/profile.yaml"))
inf("Loading profile: " + settings.profile)
common.profile = common.parse_profile(settings.profile)
if common.profile == None:
    err("Cannot load profile: profile.yaml is not valid")

if settings.debug:
    dbg("Profile content:\n"+str(common.profile))

packages = common.get_package_list(common, settings)
settings.compression = common.profile["compression"]
if "iso_merge" in common.profile:
    settings.iso_merge = common.profile["iso_merge"]

settings.show(common.profile, packages)

# distro settings
os.environ["workdir"] = settings.workdir
distro.set("workdir", settings.workdir)
distro.set("rootfs", settings.workdir+"/airootfs/")
os.chdir(settings.profile)

# distro options
distro.set("interactive", interactive)
gpg_key and distro.set("gpg", gpg_key)

distro.set("name", common.get("name"))
distro.set("arch", platform.uname().machine)
distro.set("grub_cfg", common.get("grub_cfg"))

distro.set("distro", common.get("distro"))
distro.set("label", common.get("label"))
pacman = common.get("pacman")
if os.path.exists(pacman):
    distro.set("pacman", getoutput("realpath \"{}\"".format(pacman)))
distro.set("teaiso", settings.teaiso)
distro.set("profile", settings.profile)
distro.set("packages", packages)


distro.set("rootfs", settings.rootfs)
distro.set("cmdline", common.get("linux_args"))
distro.set("workdir", settings.workdir)
distro.set("variant", common.get("variant","")) # for debian
distro.set("keyring_package", common.get("keyring_package","")) # for debian
distro.set("codename", str(common.get("codename", "testing")))  # for debian
distro.set("repository", common.get("repository"))  # for debian

def error_event():
    if settings.shared and os.path.isdir(settings.shared):
        run("umount -lf '{}/teaiso'".format(settings.rootfs))
        os.rmdir("{}/teaiso".format(settings.rootfs))
    Mount.unmount(settings.rootfs)
    

set_error_event(error_event)

if settings.debug:
    dbg("Distro options:\n"+getoutput("cat "+settings.workdir+"/options.sh"))

# airootfs creation (stage 1)
if Stage().get() < 1:
    distro.tools_init()
    distro.create_rootfs()
    Stage().set(1)
else:
    inf("Using build stage: {}".format(colorize(Stage().get(), 0)))

Mount.mount(settings.rootfs)
if settings.shared and os.path.isdir(settings.shared):
    os.mkdir("{}/teaiso".format(settings.rootfs))
    run("mount --bind '{}' '{}/teaiso'".format(settings.shared,settings.rootfs))

# Bind mount profile
if not os.path.isdir("{}/profile".format(settings.rootfs)):
    os.mkdir("{}/profile".format(settings.rootfs))
run("mount -o ro --bind '{}' '{}/profile'".format(settings.profile,settings.rootfs))

if Stage().get() < 2:
    distro.populate_rootfs()
    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory_pre")) and len(common.get("airootfs_directory_pre")) > 0:
        run("cp -af --no-preserve=ownership,mode \"{}\"/* \"{}\"/".format(settings.profile +
            "/" + common.get("airootfs_directory_pre"), settings.rootfs))
    Stage().set(2)

os.chdir(settings.workdir)
with open(settings.rootfs + '/etc/hostname', "w") as f:
    f.write(common.get("hostname","teaiso").lower())
if Stage().get() < 3:
    for i in common.get("customize_airootfs_pre", []):
        run_hook(settings, i)
    Stage().set(3)

os.chdir(settings.teaiso)

# install packages (stage 1)
if Stage().get() < 4:
    distro.install_packages()
    Stage().set(4)

# merge with airootfs directory
if Stage().get() < 5:
    inf("Copy airootfs")
    if os.path.exists(settings.profile+"/"+common.get("airootfs_directory")) and len(common.get("airootfs_directory")) > 0:
        run("cp -af --no-preserve=ownership,mode \"{}\"/* \"{}\"/".format(
            settings.profile + "/" + common.get("airootfs_directory"), settings.rootfs))

    os.chmod(settings.rootfs + '/etc/shadow',
             0o400) if os.path.exists(settings.rootfs + '/etc/shadow') else None
    os.chmod(settings.rootfs + '/etc/gshadow',
             0o400) if os.path.exists(settings.rootfs + '/etc/gshadow') else None

    # Set permissions of home and root directories if exists
    if os.path.exists(settings.rootfs + '/etc/passwd'):
        contents = open(settings.rootfs + '/etc/passwd',
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

    Stage().set(5)

# customize airootfs
if Stage().get() < 6:
    inf("Customizing airootfs")
    os.chdir(settings.workdir)
    distro.customize_airootfs()
    for i in common.get("customize_airootfs", []):
        os.chmod(settings.profile + "/" + i, 0o755)
        run_hook(settings, i)
    os.chdir(settings.teaiso)
    Stage().set(6)

# Make package list (stage 4)
if Stage().get() < 7:
    distro.make_pkglist()
    Stage().set(7)

if settings.shared and os.path.isdir(settings.shared):
    run("umount -lf '{}/teaiso'".format(settings.rootfs))
    os.rmdir("{}/teaiso".format(settings.rootfs))

# remove profile binding
run("umount -lf '{}/profile'".format(settings.rootfs))
os.rmdir("{}/profile".format(settings.rootfs))

Mount.unmount(settings.rootfs)

# Set permissions if exists
if Stage().get() < 8:
    if 'file_permissions' in common.profile:
        for name, permission in common.profile["file_permissions"].items():
            permission = permission.split(':')

            run("chown -fh -- {}:{} {}".format(
                permission[0], permission[1], settings.rootfs + "/" + name))
            run("chmod -f -- {} {}".format(permission[2],
                settings.rootfs + "/" + name))
        inf("Permissions set!")

    Stage().set(8)

# Generate IsoWork
if Stage().get() < 9:
    with open("{}/etc/machine-id".format(settings.rootfs),"w") as f:
        f.write("")
    os.chdir(settings.workdir)
    for i in common.get("customize_isowork_pre", []):
        run(i)
    os.chdir(settings.teaiso)
    common.create_isowork(settings)
    distro.clear_rootfs()
    common.create_squashfs(settings)
    os.chdir(settings.workdir)
    for i in common.get("customize_isowork", []):
        run(i)
    os.chdir(settings.teaiso)
    distro.generate_isowork()
    Stage().set(9)

# Generate Iso
if Stage().get() < 10:
    common.create_iso(settings)
    Stage().set(10)
