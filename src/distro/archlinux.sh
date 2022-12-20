# additional
write_repo(){
    if [[ "$repository" != "" ]] ; then
        echo "-r $repository"
    fi
}

# required
tools_init(){
    if [[ ! -e /usr/local/bin/archstrap ]]; then
        echo "Installing archstrap script"
        wget -c "https://gitlab.com/tearch-linux/applications-and-tools/archstrap/-/raw/master/archstrap.sh" -O archstrap
        install archstrap /usr/local/bin/
    fi
}
create_rootfs(){
    run /usr/local/bin/archstrap "$rootfs" $(write_repo)

    if [[ -f "$pacman" ]] ; then
        run install "$pacman" "$rootfs/etc/pacman.conf"
    fi
    
    # Add another mirrors
    wget -c -qO- "https://archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https&ip_version=4&use_mirror_status=on" > "$rootfs/etc/pacman.d/mirrorlist"
    run sed -i "s/^#Server/Server/" "$rootfs/etc/pacman.d/mirrorlist"
}

populate_rootfs(){
    run_in_chroot pacman-key --init
    run_in_chroot pacman-key --populate archlinux
    if ! ${interactive}; then
        run_in_chroot pacman -Syyu --noconfirm || true
    else
        run_in_chroot pacman -Syyu || true
    fi
    run_in_chroot pacman -Sy grub arch-install-scripts mkinitcpio-archiso --noconfirm

}

install_packages(){
    if ! ${interactive}; then
        run_in_chroot pacman -Syyu ${packages[@]} --noconfirm
    else
        run_in_chroot pacman -Syyu ${packages[@]}
    fi
    if [[ -d "$rootfs"/profile/packages ]] ; then
        run_in_chroot pacman -U /profile/packages/* --noconfirm
    fi

}

make_pkglist() {
    run_in_chroot pacman -Qqn >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/arch/$arch || true
    ln -s arch/$arch isowork/live || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/arch/$arch/airootfs.sfs
        cd isowork/arch/$arch; sha512sum airootfs.sfs > airootfs.sha512
        cd "${workdir}"
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/arch/$arch/airootfs.erofs
        cd isowork/arch/$arch; sha512sum airootfs.erofs > airootfs.sha512
        cd "${workdir}"
    fi
    generate_sig isowork/arch/$arch
    echo "menuentry $(distro_name) --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux archisobasedir=arch archisolabel=$label ${cmdline}" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}

customize_airootfs(){
    echo "HOOKS+=(archiso archiso_loop_mnt archiso_kms)" >> "$rootfs/etc/mkinitcpio.conf"
    for kernel in $(chroot "${rootfs}" ls /lib/modules | xargs -n1 basename); do
        run_in_chroot mkinitcpio -k "$kernel" -g "/boot/initramfs-linux.img"
    done
}

clear_rootfs(){
    find "${rootfs}/var/lib/pacman" -maxdepth 1 -type f -delete || true
    find "${rootfs}/var/lib/pacman/sync" -delete || true
    find "${rootfs}/var/cache/pacman/pkg" -type f -delete || true
    find "${rootfs}/var/log" -type f -delete || true
    find "${rootfs}/var/tmp" -mindepth 1 -delete || true
    find "${rootfs}" \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacorig' \) -delete || true
    rm -f "${rootfs}"/boot/initramfs-linux.* || true
    rm -f "${workdir}"/boot/initramfs-linux-fallback.img || true
}
