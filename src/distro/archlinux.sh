# additional
write_repo(){
    if [[ "$repository" != "" ]] ; then
        echo -r $repository
    fi
}

# required
tools_init(){
    if ! which arch-bootstrap &>/dev/null ; then
        echo "Installing arch-bootstrap script"
        wget -c "https://raw.githubusercontent.com/tokland/arch-bootstrap/master/arch-bootstrap.sh" -O arch-bootstrap.sh
        install arch-bootstrap.sh /usr/bin/arch-bootstrap
    fi
}
create_rootfs(){
    run arch-bootstrap -a "$arch" $(write_repo) "$rootfs"
    if [[ -f "$profile/pacman.conf" ]] ; then
        run install "$profile/pacman.conf" "$rootfs/etc/pacman.conf"
    fi
    run_in_chroot pacman-key --init
    run_in_chroot pacman -Syyu --noconfirm
    run_in_chroot pacman -Sy archiso --noconfirm
}

install_packages(){
    run_in_chroot pacman -Sy ${packages[@]} --noconfirm
}

make_pkglist() {
    chroot "$rootfs" pacman -Qqn >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/arch/$arch || true
    mv filesystem.squashfs isowork/arch/$arch/airootfs.sfs
    echo "menuentry Archlinux --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux archisobasedir=arch archisolabel=$label" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}

clear_rootfs(){
    find $rootfs/var/log/ -type f | xargs rm -f
}
