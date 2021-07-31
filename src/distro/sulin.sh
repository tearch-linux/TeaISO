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
    run_in_chroot inary it initrd openrc openrc-tmpfiles linux linux-firmware -y
}

install_packages(){
    run_in_chroot inary it -y ${packages[@]}
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    mv filesystem.squashfs isowork/main.sfs
    ls isowork/boot/ | grep "linux" | while read line ; do
        echo "menuentry SulinOS --class sulin {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=live" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/linux/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

clear_rootfs(){
    find $rootfs/var/log/ -type f | xargs rm -f
}
