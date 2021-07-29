from utils import run
def mount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        run("mount --bind /{0} /{1}/{0}".format(dir,rootfs))

def unmount_operations(rootfs):
    for dir in ["dev", "sys", "proc"]:
        while 0 == run("umount -lf -R /{}/{} 2>/dev/null".format(rootfs,dir)):
            True

