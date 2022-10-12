# additional
write_repo(){
    if [[ "$repository" != "" ]] ; then
        echo "-r $repository"
    else
        if [[ "$codename" == "" ]] ; then
            codename="latest-stable"
        fi
        echo http://dl-cdn.alpinelinux.org/alpine/$codename
    fi
}

# required
tools_init(){
    which apk &>/dev/null && return 0
    mkdir -p /tmp/apk
    cd /tmp/apk
    arch="$(uname -m)"
    apktools=$(wget -O - https://dl-cdn.alpinelinux.org/alpine/$codename/main/$arch/ | grep "apk-tools-static" | sed "s/^.*=\"//g;s/\".*//g")
    wget -c "https://dl-cdn.alpinelinux.org/alpine/$codename/main/$arch/$apktools" -O apk-tools-static.apk
    tar -zxf apk-tools-static.apk
    cp -pf sbin/apk.static /bin/apk
    chmod +x /bin/apk
}
create_rootfs(){
    ls ${DESTDIR}/etc/alpine-release &>/dev/null && return 0
    arch="$(uname -m)"
    apk --arch $arch -X "$(write_repo)/main/" -U --allow-untrusted --root "$rootfs" --initdb add alpine-base
    sync
    echo "$(write_repo)/main/" > "$rootfs"/etc/apk/repositories
    echo "$(write_repo)/community/" >> "$rootfs"/etc/apk/repositories
    if [[ "$codename" == "edge" ]] ; then
        echo "$(write_repo)/testing/" >> "$rootfs"/etc/apk/repositories
    fi
}

populate_rootfs(){
    cat /etc/resolv.conf > "$rootfs"/etc/resolv.conf
    run_in_chroot apk update
    run_in_chroot apk add bash ca-certificates eudev mkinitfs --allow-untrusted
    chroot "$rootfs" setup-udev || true
    cp "${teaiso}"/misc/alpine-init.sh "$rootfs"/usr/share/mkinitfs/initramfs-init-live
    echo 'features="ata base cdrom ext4 keymap kms lvm mmc nvme raid scsi squashfs usb virtio"' > "$rootfs"/etc/mkinitfs/mkinitfs-live.conf
}

customize_airootfs(){
    kernel=$(ls "$rootfs"/lib/modules/ | sort -V | head -n 1)
    if [[ "$kernel" == "" ]] ; then
                echo "Kernel missing!"
        exit 1
    fi
    run_in_chroot mkinitfs -i /usr/share/mkinitfs/initramfs-init-live -c /etc/mkinitfs/mkinitfs-live.conf -o /boot/initramfs-live "$kernel"
}

clear_rootfs(){
    rm -rf $rootfs/var/cache/apk/* || true
    find "$rootfs/var/log/" -type f | xargs rm -f  || true
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live/ || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/
        cd isowork/live; sha512sum filesystem.squashfs > filesystem.sha512
        cd "${workdir}"
    fi
    echo "menuentry $(distro_name) --class alpine {" >> isowork/boot/grub/grub.cfg
    if [[ -f isowork/boot/vmlinuz-lts ]] ; then
        echo "  linux /boot/vmlinuz-lts boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
    elif [[ -f isowork/boot/vmlinuz-edge ]] ; then
        echo "  linux /boot/vmlinuz-edge boot=live ${cmdline}" >> isowork/boot/grub/grub.cfg
    else
        echo "Kernel missing!"
        exit 1
    fi
    echo "  initrd /boot/initramfs-live" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}

install_packages(){
    run_in_chroot apk add ${packages[@]}
    if [[ -d "$rootfs"/profile/packages ]] ; then
        run_in_chroot apk add --allow-untrusted /profile/packages/*
    fi
}
make_pkglist() {
    run_in_chroot apk list >  ${workdir}/packages.list
}
