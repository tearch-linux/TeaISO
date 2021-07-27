import yaml
import os
from utils import err
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
    validation = validate_profile()
    
    if not validation[0]:
       err("Key not defined in profile:\n -> {}".format(validation[1])) 
    
    return profile

def validate_profile():
    global profile
    required_keys = ['name', 'publisher', 'label', 'application_id', 'airootfs_directory', 'arch', 'grub_cfg', 'packages', 'distro']

    for key in required_keys:
        if key not in profile:
            return None, key
        
    return [True]

def get(key,default=""):
    if key in profile:
        return profile[key]
    return default
