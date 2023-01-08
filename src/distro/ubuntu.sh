source "$teaiso"/distro/debian.sh
typeset -r populate_rootfs
typeset -r generate_isowork
typeset -r create_rootfs

create_rootfs(){
    if [[ "$codename" == "latest" ]] ; then
        codename=$(wget -O - https://cdimage.ubuntu.com/daily-live/current/  | grep "desktop-amd64.iso" | head -n 1 | sed "s/.*href=\"//g" | sed "s/-.*//g")
    fi
    if [[ ! -e /usr/share/debootstrap/scripts/${codename} ]] ; then
        ln -s sid /usr/share/debootstrap/scripts/${codename}
    fi
    if ! run debootstrap --arch=$(get_arch $arch) --no-check-gpg --no-merged-usr --exclude="usrmerge,usr-is-merged" --extractor=ar "$codename" "$rootfs" "$repository" ; then
        cat $rootfs/debootstrap/debootstrap.log
        exit 1
    fi
    echo -e "#!/bin/sh\nexit 101" > "$rootfs"/usr/sbin/policy-rc.d
    chmod +x "$rootfs"/usr/sbin/policy-rc.d
    run_in_chroot apt install -f -yq --force-yes
    if [[ "" != "${keyring_package}" ]] ; then
        run_in_chroot apt install ${keyring_package} -yq --force-yes
    fi
    if [[ -f "$rootfs"/usr/bin/bash ]] ; then
        install "${teaiso}"/misc/usrparse.sh "$rootfs"/tmp/usrparse.sh
        run_in_chroot bash /tmp/usrparse.sh
    fi
    #### Disable recommends by default
    echo 'APT::Install-Recommends "0";' > "$rootfs"/etc/apt/apt.conf.d/01norecommend
    echo 'APT::Install-Suggests "0";' >> "$rootfs"/etc/apt/apt.conf.d/01norecommend
}

populate_rootfs(){
    run_in_chroot apt update -yq
    run_in_chroot apt full-upgrade -o Dpkg::Options::="--force-confnew" -yq
    run_in_chroot apt install casper -o Dpkg::Options::="--force-confnew" -yq --force-yes
    mkdir -p "$rootfs"/etc/fonts/
    touch "$rootfs"/etc/fonts/fonts.conf
    mkdir -p "$rootfs"/boot/grub
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/casper/ || true
    ln -s capser isowork/live
    ln -s . isowork/ubuntu || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/casper/
        cd isowork/casper; sha512sum filesystem.squashfs > filesystem.sha512
        cd "${workdir}"
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/casper/
        cd isowork/casper; sha512sum filesystem.erofs > filesystem.sha512
        cd "${workdir}"
    fi
    generate_sig isowork/casper
    ls isowork/boot/ | grep "vmlinuz" | while read line ; do
        echo "menuentry $(distro_name) --class debian {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=casper ${cmdline}" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}
