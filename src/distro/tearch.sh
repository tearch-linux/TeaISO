source "$teaiso"/distro/archlinux.sh

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
    mkdir -p isowork/arch/$arch || true
    mv filesystem.squashfs isowork/arch/$arch/airootfs.sfs
    echo "menuentry Tearch-linux --class arch {" >> isowork/boot/grub/grub.cfg
    echo "  linux /boot/vmlinuz-linux boot=live" >> isowork/boot/grub/grub.cfg
    echo "  initrd /boot/initramfs-linux.img" >> isowork/boot/grub/grub.cfg
    echo "}" >> isowork/boot/grub/grub.cfg
}
