# required
tools_init(){
    if ! which ympstrap &>/dev/null ; then
        wget https://gitlab.com/turkman/devel/sources/ymp/-/raw/master/scripts/ympstrap -O /usr/bin/ympstrap
        chmod +x /usr/bin/ympstrap
    fi
}

create_rootfs(){
    ympstrap "$rootfs"
    mkdir -p "$rootfs/"{dev,sys,proc,run,tmp,etc,boot}
    touch "$rootfs/etc/shadow"
}

populate_rootfs(){
    run_in_chroot ymp repo --update --ignore-gpg --allow-oem
    run_in_chroot ymp install linux live-boot --ignore-gpg --allow-oem --no-emerge
}

install_packages(){
    if [[ -d "$rootfs"/profile/packages ]] ; then
        run_in_chroot ymp install --allow-oem --no-emerge /profile/packages/*.inary
    fi
}

make_pkglist() {
    run_in_chroot ymp list --installed >  ${workdir}/packages.list
}
generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live/ || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/
        cd isowork/live; sha512sum filesystem.squashfs > filesystem.sha512
        cd "${workdir}"
    fi
    ls isowork/boot/ | grep "vmlinuz" | while read line ; do
        echo "menuentry $(distro_name) --class turkman {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}
customize_airootfs(){
    for kernel in $(ls "$rootfs"/lib/modules/) ; do
        run_in_chroot update-initramfs -u -k $kernel
    done
}

clear_rootfs(){
    run_in_chroot ymp clean
}
