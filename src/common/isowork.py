import os
from utils import getoutput, run, inf
def create_isowork(settings):
    if not os.path.exists("{}/isowork/boot/grub".format(settings.workdir)):
        os.makedirs("{}/isowork/boot/grub".format(settings.workdir))
    for i in os.listdir("{}/boot".format(settings.rootfs)):
        run("cp -pf {}/boot/{} {}/isowork/boot".format(settings.rootfs,i,settings.workdir))

def create_iso(settings):
    inf("Creating iso file.")
    run("grub-mkrescue {}/isowork -o {}/teaiso.iso".format(settings.workdir, settings.output))

def create_squashfs(settings):
    inf("Creating squashfs file.")
    if os.path.exists("{}/filesystem.squashfs".format(settings.workdir)):
        os.unlink("{}/filesystem.squashfs".format(settings.workdir))
    run("mksquashfs {} {}/filesystem.squashfs -comp gzip -wildcards".format(settings.rootfs, settings.workdir))
