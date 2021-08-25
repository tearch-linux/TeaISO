# required
tools_init(){
    return
}

create_rootfs(){
    mkdir -p "$rootfs/"{dev,sys,proc,run,tmp,etc,boot}
    touch "$rootfs/etc/shadow"
}

populate_rootfs(){
    return
}

install_packages(){
    return
}

make_pkglist() {
    touch ${workdir}/packages.list
}

generate_isowork(){
    if [[ -f "$grub_cfg" ]]; then
        cat $grub_cfg > isowork/boot/grub/grub.cfg
    else
        echo "insmod all_video" > isowork/boot/grub/grub.cfg
    fi
}

customize_airootfs(){
    return
}

clear_rootfs(){
    return
}
