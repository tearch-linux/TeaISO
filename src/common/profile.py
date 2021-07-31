import yaml
import os
from utils import err
profile=None
def parse_profile(file="/usr/lib/teaiso/profile/baseline/profile.yaml",teaiso="/usr/lib/teaiso"):
    global profile
    if os.path.exists(teaiso+"/profiles/"+file):
        file = teaiso+"/profiles/"+file
    if not os.path.exists(file):
        return None
    
    contents = {}
    with open(file, "r") as file:
        try:
            contents = yaml.load(file.read(), Loader=yaml.FullLoader)
        except BaseException:
            contents = yaml.load(file.read())
            
    if 'file_permissions' in contents:
            file_permissions = {}
            for file in contents["file_permissions"]:
                file = file.split("|")
                file_permissions[file[0]] = file[1]
            contents["file_permissions"] = file_permissions
        
    profile=contents
    validation = validate_profile()
    
    if not validation[0]:
       err("Key not defined in profile:\n -> {}".format(validation[1])) 
    
    return profile

def validate_profile():
    global profile
    required_keys = ['name', 'publisher', 'label', 'application_id', 'arch', 'grub_cfg', 'packages', 'distro']

    for key in required_keys:
        if key not in profile:
            return None, key
        
    return [True]

def get(key,default=""):
    if key in profile:
        return profile[key]
    return default

def get_package_list(common,settings):
    for file in common.get("packages"):
        file = settings.profile + "/" + file
    
        if not os.path.exists(file):
            warn("Packages file not exists:\n -> {}".format(file))
    
        packages = []
        with open(file, "r") as f:
            for line in f.read().split("\n"):
                if not line.startswith("#"):
                    packages.append(line.strip())
    return packages
