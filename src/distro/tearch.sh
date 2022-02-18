source "$teaiso"/distro/archlinux.sh
typeset -r populate_rootfs
typeset -r generate_isowork

populate_rootfs(){
    wget https://gitlab.com/tearch-linux/configs/tearch-mirrorlist/-/raw/master/tearch-mirrorlist -O "$rootfs/etc/pacman.d/tearch-mirrorlist"
    run_in_chroot pacman-key --init
    run_in_chroot pacman-key --populate archlinux
    if ! ${interactive}; then
        run_in_chroot pacman -Syyu --noconfirm || true
    else
        run_in_chroot pacman -Syyu || true
    fi
    run_in_chroot pacman -Sy mkinitcpio-teaiso grub --noconfirm
}

customize_airootfs(){
    echo "HOOKS+=(live_hook)" >> "$rootfs/etc/mkinitcpio.conf"
    for kernel in $(chroot "${rootfs}" ls /lib/modules | xargs -n1 basename); do
        run_in_chroot mkinitcpio -k "$kernel" -g "/boot/initramfs-linux.img"
    done
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live isowork/arch || true
    ln -s ../live isowork/arch/$arch || true
    if [[ -e "filesystem.squashfs" ]]; then
        mv filesystem.squashfs isowork/live/airootfs.sfs
        cd isowork/live; sha512sum airootfs.sfs > airootfs.sha512
        cd "${workdir}"
    elif [[ -e "filesystem.erofs" ]]; then
        mv filesystem.erofs isowork/live/airootfs.erofs
        cd isowork/live; sha512sum airootfs.sfs > airootfs.sha512
        cd "${workdir}"
    fi
    generate_sig isowork/live
    echo "menuentry $(distro_name) --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux boot=live live-config ${cmdline}" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}
