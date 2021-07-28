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
}

install_packages(){
    run_in_chroot pacman -Sy ${packages[@]} --noconfirm
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
}
