from utils import inf
import os
def get_stage():
    workdir = os.environ["workdir"]
    if not os.path.exists("{}/stage".format(workdir)):
        set_stage(0)
        return 0
    with open("{}/stage".format(workdir),"r") as f:
        return int(f.read())

def set_stage(stage):
    workdir = os.environ["workdir"]
    inf("Stage:{} done.".format(stage))
    with open("{}/stage".format(workdir),"w") as f:
        return f.write(str(stage))
