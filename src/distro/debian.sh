# additional
get_arch(){
    [[ "$1" == "x86_64" ]] && echo amd64
    [[ "$1" == "i686" ]] && echo i386
    [[ "$1" == "aarch64" ]] && echo arm64
}
export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true

# required
tools_init(){
    if ! which debootstrap &>/dev/null ; then
        echo "Installing debootstrap script"
        wget -c "https://salsa.debian.org/installer-team/debootstrap/-/archive/master/debootstrap-master.zip" -O debootstrap.zip
        unzip debootstrap.zip
        cd debootstrap-master
        make && make install
    fi
}

create_rootfs(){
    if ! run debootstrap --arch=$(get_arch $arch) --no-check-gpg --no-merged-usr --exclude=usrmerge --extractor=ar ${variant:+--variant=$variant} "$codename" "$rootfs" "$repository" ; then
        cat "$rootfs"/debootstrap/debootstrap.log
        exit 1
    fi
    echo -e "#!/bin/sh\nexit 101" > "$rootfs"/usr/sbin/policy-rc.d
    chmod +x "$rootfs"/usr/sbin/policy-rc.d
    if [[ "" != "${keyring_package}" ]] ; then
        run_in_chroot apt install ${keyring_package} -yq
    fi
}

populate_rootfs(){
    run_in_chroot apt update -yq
    run_in_chroot apt full-upgrade -yq
    run_in_chroot apt install live-boot live-config user-setup -yq
}

install_packages(){
    run_in_chroot apt update -yq
    run_in_chroot apt install -yq -o Dpkg::Options::="--force-confnew" ${packages[@]}
}

make_pkglist() {
    run_in_chroot apt list --installed >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live/ || true
    ln -s live isowork/casper || true
    ln -s . isowork/debian || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/
        cd isowork/live; sha512sum filesystem.squashfs > filesystem.sha512
        cd "${workdir}"
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/live/
        cd isowork/live; sha512sum filesystem.erofs > filesystem.sha512
        cd "${workdir}"
    fi
    generate_sig isowork/live
    ls isowork/boot/ | grep "vmlinuz" | while read line ; do
        echo "menuentry $(distro_name) --class debian {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

customize_airootfs(){
    run_in_chroot update-initramfs -u -k all
}

clear_rootfs(){
    run_in_chroot apt clean
    run_in_chroot apt autoremove --purge
    rm -rf $rootfs/var/lib/apt/lists || true
    find "$rootfs/var/log/" -type f | xargs rm -f  || true
}
