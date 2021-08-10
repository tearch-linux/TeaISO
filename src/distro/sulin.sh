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

populate_rootfs(){
    run_in_chroot inary it initrd openrc openrc-tmpfiles -y
}

install_packages(){
    run_in_chroot inary it -y ${packages[@]}
}

make_pkglist() {
    run_in_chroot inary li >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/main.sfs
        cd isowork/live; sha512sum main.sfs > main.sha512; cd -
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/live/main.erofs
        cd isowork/live; sha512sum main.sfs > main.sha512; cd -
    fi
    generate_sig isowork/live
    ls "$rootfs/kernel/modules/" | while read line ; do
        echo "menuentry $(distro_name) --class sulin {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/linux-$line boot=live" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/initrd.img-$line" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

customize_airootfs(){
    ls "$rootfs/kernel/modules/" | while read line ; do
        run_in_chroot update-initrd KERNELVER="$line"
    done
}

clear_rootfs(){
    find "$rootfs/var/log/" -type f | xargs rm -f || true
    run_in_chroot inary dc
    run_in_chroot inary hs -r
}
