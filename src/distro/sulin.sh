# required
tools_init(){
    if ! which arch-bootstrap &>/dev/null ; then
        echo "Installing sulinstrapt script"
        wget -c "https://gitlab.com/sulinos/devel/inary/-/raw/develop/scripts/sulinstrapt" -O sulinstrapt.sh
        install sulinstrapt.sh /usr/bin/sulinstrapt
    fi
}
create_rootfs(){
    run sulinstrapt "$rootfs"
}

populate_chroot(){
    run_in_chroot inary it initrd openrc openrc-tmpfiles -y
}

install_packages(){
    run_in_chroot inary it -y ${packages[@]}
}

make_pkglist() {
    chroot "$rootfs" inary li >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    mv filesystem.squashfs isowork/main.sfs
    ls "$rootfs/kernel/modules/" | while read line ; do
        echo "menuentry SulinOS --class sulin {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/linux-$line boot=live" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/initrd.img-$line" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

customize_airootfs(){
    ls "$rootfs/kernel/modules/" | while read line ; do
        chroot "$rootfs" update-initrd KERNELVER="$line"
    done
}

clear_rootfs(){
    find "$rootfs/var/log/" -type f | xargs rm -f
    chroot "$rootfs" inary dc
    chroot "$rootfs" inary hs -r
}
