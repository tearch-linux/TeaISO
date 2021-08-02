from utils import run, inf
def mount_operations(rootfs):
    for dir in ["dev", "dev/pts", "sys", "proc", "run"]:
        run("mount --bind /{1} /{0}/{1} 2>/dev/null".format(rootfs,dir))

def unmount_operations(rootfs):
    for dir in ["dev/pts", "dev", "sys", "proc", "run"]:
        while 0 == run("umount -lf -R /{}/{}".format(rootfs,dir),vital=False):
            True

