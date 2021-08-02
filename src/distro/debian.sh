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
    if ! run debootstrap --arch=$(get_arch $arch) --no-check-gpg --no-merged-usr --exclude=usrmerge --extractor=ar "$codename" "$rootfs" "$repository" ; then
        cat $rootfs/debootstrap/debootstrap.log
        exit 1
    fi
}

populate_rootfs(){
    run_in_chroot apt install live-boot live-config -yq
}

install_packages(){
    run_in_chroot apt update -yq
    run_in_chroot apt install -yq -o Dpkg::Options::="--force-confnew" ${packages[@]}
}

make_pkglist() {
    chroot "$rootfs" apt list --installed >  ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live/ || true
    mv filesystem.squashfs isowork/live/
    ls isowork/boot/ | grep "vmlinuz" | while read line ; do
        echo "menuentry Debian --class debian {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=live" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}

customize_airootfs(){
    chroot "$rootfs" update-initramfs -u -k all
}

clear_rootfs(){
    run_in_chroot apt clean
    run_in_chroot apt autoremove
    rm -rf $rootfs/var/lib/apt/lists
    find "$rootfs/var/log/" -type f | xargs rm -f
}
