import yaml
import os, platform
from datetime import date
from utils import err, warn, versiontuple
profile = None


def parse_profile(profile_dir="/usr/lib/teaiso/profile/archlinux", teaiso="/usr/lib/teaiso"):
    global profile
    if not os.path.exists(profile_dir + "/profile.yaml"):
        return None

    contents = {}
    with open(profile_dir + "/profile.yaml", "r") as file:
        if versiontuple(3.13) >= versiontuple(yaml.__version__) :
            contents = yaml.load(file.read())
        else:
            contents = yaml.load(file.read(), Loader=yaml.FullLoader)
    if contents == None or contents == {}:
        err("Failed to load profile.yaml file.")

    if 'file_permissions' in contents:
        file_permissions = {}
        for file in contents["file_permissions"]:
            file = file.split("|")
            file_permissions[file[0]] = file[1]
        contents["file_permissions"] = file_permissions

    if 'compression' in contents:
        contents["compression"] = contents["compression"].split("||")
    else:
        contents["compression"] = ['squashfs', '-comp gzip']

    contents["grub_cfg"] = os.path.realpath(
        profile_dir + "/" + contents["grub_cfg"])
    contents["iso_name"] = contents["name"] + "-" + \
        date.today().strftime("%d-%m-%Y") + "-" + platform.uname().machine + ".iso"

    profile = contents
    validation = validate_profile(profile)

    if not validation[0]:
        err("Key not defined in profile:\n -> {}".format(validation[1]))

    return profile


def validate_profile(profile):
    required_keys = ['name', 'publisher', 'label',
                     'application_id', 'grub_cfg', 'packages', 'distro']

    for key in required_keys:
        if key not in profile:
            return None, key

    return [True]


def get(key, default=""):
    if key in profile:
        return profile[key]
    return default


def get_package_list(common, settings):
    packages = []
    for file in common.get("packages"):
        file = settings.profile + "/" + file

        if not os.path.exists(file):
            warn("Packages file not exists:\n -> {}".format(file))

        with open(file, "r") as f:
            for line in f.read().split("\n"):
                if not line.startswith("#"):
                    packages.append(line.strip())
    return packages
