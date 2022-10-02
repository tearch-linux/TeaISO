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
    if [[ -d "$rootfs"/profile/packages ]] ; then
        run_in_chroot inary it /profile/packages/*.inary
    fi
}

make_pkglist() {
    run_in_chroot inary li >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    fi
    ln -s ../ isowork/live || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/main.sfs
        cd isowork; sha512sum main.sfs > main.sha512
        cd "${workdir}"
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/live/main.erofs
        cd isowork; sha512sum main.sfs > main.sha512
        cd "${workdir}"
    fi
    generate_sig isowork
    ls "$rootfs/kernel/modules/" | while read line ; do
        echo "menuentry $(distro_name) --class sulin {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/linux-$line boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
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
