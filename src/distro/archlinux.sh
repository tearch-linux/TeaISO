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

    if [[ -f "$pacman" ]] ; then
        run install "$pacman" "$rootfs/etc/pacman.conf"
    fi
}

populate_rootfs(){
    run_in_chroot pacman-key --init
    run_in_chroot pacman-key --populate archlinux
    if ! ${interactive}; then
        run_in_chroot pacman -Syyu --noconfirm || true
    else
        run_in_chroot pacman -Syyu || true
    fi
    run_in_chroot pacman -Sy grub arch-install-scripts --noconfirm

}

install_packages(){
    if ! ${interactive}; then
        run_in_chroot pacman -Sy ${packages[@]} --noconfirm
    else
        run_in_chroot pacman -Sy ${packages[@]}
    fi
}

make_pkglist() {
    run_in_chroot pacman -Qqn >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/arch/$arch || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/arch/$arch/airootfs.sfs
        cd isowork/arch/$arch; sha512sum airootfs.sfs > airootfs.sha512; cd -
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/arch/$arch/airootfs.erofs
        cd isowork/arch/$arch; sha512sum airootfs.erofs > airootfs.sha512; cd -
    fi
    generate_sig isowork/arch/$arch
    echo "menuentry $(distro_name) --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux archisobasedir=arch archisolabel=$label" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}

customize_airootfs(){
    for kernel in $(chroot "${rootfs}" ls /etc/mkinitcpio.d/*.preset | xargs -n1 basename); do
        run_in_chroot mkinitcpio -p "${kernel%.preset}"
    done
}

clear_rootfs(){
    find "${rootfs}/var/lib/pacman" -maxdepth 1 -type f -delete || true
    find "${rootfs}/var/lib/pacman/sync" -delete || true
    find "${rootfs}/var/cache/pacman/pkg" -type f -delete || true
    find "${rootfs}/var/log" -type f -delete || true
    find "${rootfs}/var/tmp" -mindepth 1 -delete || true
    find "${rootfs}" \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacorig' \) -delete || true

    echo "" > "$rootfs/etc/machine-id" || true
}
