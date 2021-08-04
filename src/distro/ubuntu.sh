source "$teaiso"/distro/debian.sh
typeset -r populate_rootfs
typeset -r generate_isowork
typeset -r create_rootfs

create_rootfs(){
    if [[ "$codename" == "latest" ]] ; then
        codename=$(curl https://cdimage.ubuntu.com/daily-live/current/  | grep "desktop-amd64.iso" | head -n 1 | sed "s/.*href=\"//g" | sed "s/-.*//g")
    fi
    if ! run debootstrap --arch=$(get_arch $arch) --no-check-gpg --no-merged-usr --exclude=usrmerge --extractor=ar "$codename" "$rootfs" "$repository" ; then
        cat $rootfs/debootstrap/debootstrap.log
        exit 1
    fi
}

populate_rootfs(){
    run_in_chroot apt install casper -yq
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
        echo "menuentry $(distro_name) --class debian {" >> isowork/boot/grub/grub.cfg
        echo "  linux /boot/$line boot=casper" >> isowork/boot/grub/grub.cfg
        echo "  initrd /boot/$(echo $line | sed s/vmlinuz/initrd.img/g)" >> isowork/boot/grub/grub.cfg
        echo "}" >> isowork/boot/grub/grub.cfg
    done
}
