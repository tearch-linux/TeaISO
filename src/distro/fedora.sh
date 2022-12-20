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
    run_in_chroot dnf install -y --nogpgcheck kernel-core kernel-modules dracut-live busybox

}

install_packages(){
    run_in_chroot dnf install -y --nogpgcheck ${packages[@]}
    if [[ -d "$rootfs"/profile/packages ]] ; then
        run_in_chroot rpm -i /profile/packages/*.rpm
    fi
}

make_pkglist() {
    # fixme
    : > ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live/ || true
    ln -s . isowork/fedora || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/
        cd isowork/live; sha512sum filesystem.squashfs > filesystem.sha512
        cd "${workdir}"
    fi
    generate_sig isowork/live
    ls isowork/boot/ | grep "vmlinuz" | while read line ; do
        echo "menuentry $(distro_name) --class fedora {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initramfs/g).img" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

customize_airootfs(){
    # Replace dracut init with custom init
    # Fedora init is too bloat and complex.
    install "${teaiso}"/misc/replace-init-initramfs.sh "$rootfs"/bin/replace-init-initramfs.sh
    install "${teaiso}"/misc/alpine-init.sh "$rootfs"/etc/fdinit-teaiso.sh
    run_in_chroot bash /bin/replace-init-initramfs.sh /etc/fdinit-teaiso.sh
    run_in_chroot usermod -p $(openssl passwd live) root
}

clear_rootfs(){
    find "${rootfs}/var/log" -type f -delete || true
    find "${rootfs}/var/tmp" -mindepth 1 -delete || true
    find "${rootfs}" \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacorig' \) -delete || true
}
