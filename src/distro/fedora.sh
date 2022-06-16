# additional
write_repo(){
    if [[ "$repository" != "" ]] ; then
        echo "-r $repository"
    fi
}

# required
tools_init(){
    if [[ ! -e /usr/local/bin/fdstrap ]]; then
        echo "Installing fdstrap script"
        wget -c "https://gitlab.com/tearch-linux/applications-and-tools/fdstrap/-/raw/main/fdstrap.sh" -O fdstrap
        install fdstrap /usr/local/bin/
    fi
}
create_rootfs(){
    if [[ "$codename" == "" ]] ; then
        codename=rawhide
    fi
    run /usr/local/bin/fdstrap "$rootfs" -v "$codename"
    rm -f "$rootfs"/etc/resolv.conf
    cat /etc/resolv.conf >> "$rootfs"/etc/resolv.conf
}

populate_rootfs(){
    run_in_chroot dnf install dracut-live -y

}

install_packages(){
    run_in_chroot dnf install -y ${packages[@]}
}

make_pkglist() {
    : #fixme
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
    fi
    generate_sig isowork/arch/$arch
    echo "menuentry $(distro_name) --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux archisobasedir=arch archisolabel=$label ${cmdline}" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}

customize_airootfs(){
    : #fixme
}

clear_rootfs(){
    find "${rootfs}/var/log" -type f -delete || true
    find "${rootfs}/var/tmp" -mindepth 1 -delete || true
    find "${rootfs}" \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacorig' \) -delete || true

    echo "" > "$rootfs/etc/machine-id" || true
}
