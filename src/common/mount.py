from utils import run, inf
def mount_operations(rootfs):
    run("mount -t proc proc {}/proc/".format(rootfs))
    run("mount --rbind /sys {}/sys/".format(rootfs))
    run("mount --rbind /dev {}/dev/".format(rootfs))
    run("mount --rbind /run {}/run/".format(rootfs))

def unmount_operations(rootfs):
    for dir in ["dev/pts", "dev", "sys", "proc", "run"]:
        while 0 == run("umount -lf -R /{}/{} 2>/dev/null".format(rootfs,dir)):
            True

