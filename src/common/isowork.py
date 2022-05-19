import os
from utils import getoutput, run, inf, err, VERSION
from datetime import date, datetime
from common import get
import shutil
import subprocess


compression_tool = "squashfs"


def create_isowork(settings):
    if os.path.exists("{}/isowork/".format(settings.workdir)):
        run("rm -rf -- {}/isowork".format(settings.workdir))
    os.makedirs("{}/isowork/".format(settings.workdir))
    if settings.iso_merge:
        run("cp -rf {}/* {}/isowork/".format(settings.profile + "/" + settings.iso_merge,
            settings.workdir))
    if not os.path.exists("{}/isowork/boot/grub".format(settings.workdir)):
        os.makedirs("{}/isowork/boot/grub".format(settings.workdir))
    for i in os.listdir("{}/boot".format(settings.rootfs)):
        if os.path.isfile("{}/boot/{}".format(settings.rootfs, i)):
            run("cp -f {}/boot/{} {}/isowork/boot".format(settings.rootfs,
                i, settings.workdir))

    shutil.copyfile(settings.workdir + "/packages.list",
                    settings.workdir + "/isowork/packages.list")


def create_iso(settings):
    inf("Creating iso file.")
    if not os.path.exists("{}/isowork/EFI/boot".format(settings.workdir)):
        os.makedirs("{}/isowork/EFI/boot".format(settings.workdir))

    # Copy Necessary Directories
    for bootloader in ["i386-pc", "i386-efi", "x86_64-efi", "themes"]:
        if os.path.isdir("{}/usr/lib/grub/i386-pc/".format(settings.rootfs)):
            run("cp -r {}/usr/lib/grub/{}/ {}/isowork/boot/grub/".format(settings.rootfs,
                bootloader, settings.workdir), vital=False)
        else:
            run("cp -r /usr/lib/grub/{}/ {}/isowork/boot/grub/".format(bootloader,
                settings.workdir), vital=False)

    # Generate Bootloaders
    run("grub-mkimage -d {0}/isowork/boot/grub/i386-pc/ -o {0}/isowork/boot/grub/i386-pc/core.img -O i386-pc -p /boot/grub biosdisk iso9660".format(settings.workdir), vital=False)
    run("cat {0}/isowork/boot/grub/i386-pc/cdboot.img {0}/isowork/boot/grub/i386-pc/core.img > {0}/isowork/boot/grub/i386-pc/eltorito.img".format(settings.workdir), vital=False)
    run("grub-mkimage -d {0}/isowork/boot/grub/x86_64-efi/ -o {0}/isowork/EFI/boot/bootx64.efi -O x86_64-efi -p /boot/grub iso9660".format(
        settings.workdir), vital=False)
    run("grub-mkimage -d {0}/isowork/boot/grub/i386-efi/ -o {0}/isowork/EFI/boot/bootia32.efi -O i386-efi -p /boot/grub iso9660".format(
        settings.workdir), vital=False)

    # Generate efi.img
    run("dd if=/dev/zero of=\"{}/isowork/efi.img\" bs=4M count=1 oflag=sync".format(settings.workdir))
    run("mkfs.vfat -n TEAISO_EFI {}/isowork/efi.img &>/dev/null".format(settings.workdir))
    os.sync() # Call sync for efi image.
    run("mmd -i {}/isowork/efi.img ::/EFI".format(settings.workdir))
    run("mmd -i {}/isowork/efi.img ::/EFI/boot".format(settings.workdir))
    run("mcopy -i {0}/isowork/efi.img {0}/isowork/EFI/boot/* ::/EFI/boot".format(settings.workdir))

    # Generate writable
    run("dd if=/dev/zero of=\"{}/writable.img\" bs=4M count=1 oflag=sync".format(settings.workdir))
    run("mkfs.ext4 -b 1024 -L writable \"{}/writable.img\"".format(settings.workdir))
    
    # Miscellaneous
    if not os.path.exists(settings.output):
        os.mkdir(settings.output)

    run("grub-editenv {}/isowork/boot/grub/grubenv set menu_show_once=1".format(settings.workdir))

    # md5sums.txt file
    run("cd {0}/isowork ; find . -type f | xargs md5sum | sort -V > {0}/isowork/md5sums.txt".format(settings.workdir))

    modification_date = datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S-00").replace("-", "")
    run("""xorriso -as mkisofs \
                --modification-date={0} \
                --protective-msdos-label \
                -volid "{1}" \
                -appid "{2}" \
                -publisher "{3}" \
                -preparer "Prepared by TeaISO v{4}" \
                -r -graft-points -no-pad \
                --sort-weight 0 / \
                --sort-weight 1 /boot \
                --grub2-mbr {5}/isowork/boot/grub/i386-pc/boot_hybrid.img \
                -iso_mbr_part_type 0x83 \
                -isohybrid-gpt-basdat \
                -partition_offset 16 \
                -b boot/grub/i386-pc/eltorito.img \
                -c boot.catalog \
                -no-emul-boot -boot-load-size 4 -boot-info-table --grub2-boot-info \
                -eltorito-alt-boot \
                -append_partition 2 0xef {5}/isowork/efi.img \
                -append_partition 3 0x83 {5}/writable.img \
                -e --interval:appended_partition_2:all:: \
                -no-emul-boot \
                --mbr-force-bootable \
                -apm-block-size 512 \
                -partition_cyl_align off \
                -full-iso9660-filenames \
                -iso-level 3 -rock -joliet \
                -o {6} \
                {5}/isowork/""".format(modification_date, get("label"), get("application_id"),
                                       get("publisher"), VERSION, settings.workdir,
                                       settings.output + "/" + get("iso_name")))


def create_squashfs(settings):
    inf("Creating airootfs file.")
    if settings.compression[0] == "squashfs":
        if os.path.exists("{}/filesystem.squashfs".format(settings.workdir)):
            os.unlink("{}/filesystem.squashfs".format(settings.workdir))
        run("mksquashfs {} {}/filesystem.squashfs {} -always-use-fragments -b 65536 -wildcards".format(
            settings.rootfs, settings.workdir, settings.compression[1]))
    elif settings.compression[0] == "erofs":
        if os.path.exists("{}/filesystem.erofs".format(settings.workdir)):
            os.unlink("{}/filesystem.erofs".format(settings.workdir))
        uuid = subprocess.check_output(
            "uuidgen --sha1 --namespace 93a870ff-8565-4cf3-a67b-f47299271a96 --name $(date +%s)", shell=True).decode("UTF-8").strip()
        run("mkfs.erofs -U {} {} -- {}/filesystem.erofs \"{}\"".format(uuid,
            settings.compression[1], settings.workdir, settings.rootfs))
    else:
        err("Valid compression tool not found! Please, check your profile.")
