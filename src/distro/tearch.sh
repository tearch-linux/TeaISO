source "$teaiso"/distro/archlinux.sh
typeset -r populate_rootfs
typeset -r generate_isowork

populate_rootfs(){
    run wget https://gitlab.com/tearch-linux/configs/tearch-mirrorlist/-/raw/master/tearch-mirrorlist -O "$rootfs/etc/pacman.d/tearch-mirrorlist"
    run_in_chroot pacman-key --init
    run_in_chroot pacman-key --populate archlinux
    run_in_chroot pacman -Syyu --noconfirm || true
    run_in_chroot pacman -Sy mkinitcpio-teaiso grub --noconfirm
}

generate_isowork(){
    if [[ -f "$profile/grub.cfg" ]] ; then
        cat $profile/grub.cfg > isowork/boot/grub/grub.cfg
    fi
    mkdir -p isowork/live || true
    mv filesystem.squashfs isowork/live/airootfs.sfs
    echo "menuentry $(distro_name) --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux boot=live live-config" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}
