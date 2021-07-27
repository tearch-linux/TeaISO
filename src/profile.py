import yaml
import os

def parse_profile(file):
    if not os.path.exists(file):
        return None
    
    contents = {}
    with open(file, "r") as file:
        try:
            contents = yaml.load(file.read(), Loader=yaml.FullLoader)
        except BaseException:
            contents = yaml.load(file.read())
    return contents