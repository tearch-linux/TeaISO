from utils import run, inf
def mount_operations(rootfs):
    for dir in ["dev", "dev/pts", "sys", "proc", "run"]:
        run("mount --bind /{1} /{0}/{1} 2>/dev/null".format(rootfs,dir))
    run("ln -s {0}/proc/self/fd {0}/dev/fd 2>/dev/null".format(rootfs),vital=False)
    run("ln -s {0}/proc/self/mounts /etc/mtab")

def unmount_operations(rootfs):
    for dir in ["dev/pts", "dev", "sys", "proc", "run"]:
        while 0 == run("umount -lf -R /{}/{}".format(rootfs,dir),vital=False):
            True

