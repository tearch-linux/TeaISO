import yaml
import os
profile=None
def parse_profile(file="/usr/lib/teaiso/profile/baseline/profile.yaml"):
    global profile
    if not os.path.exists(file):
        return None
    
    contents = {}
    with open(file, "r") as file:
        try:
            contents = yaml.load(file.read(), Loader=yaml.FullLoader)
        except BaseException:
            contents = yaml.load(file.read())
    profile=contents
    validate_profile()
    return profile

def validate_profile():
    global profile
    required_keys = ['name', 'publisher', 'label', 'application_id', 'airootfs_directory', 'arch', 'grub_cfg', 'packages', 'distro']
    
    for key in required_keys:
        if key not in profile:
            return None, key
        
    return True

def get(key,default=""):
    if key in profile:
        return profile[key]
    return default
