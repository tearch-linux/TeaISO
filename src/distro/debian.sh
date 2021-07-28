# additional
get_arch(){
    [[ "$1" == "x86_64" ]] && echo amd64
    [[ "$1" == "i686" ]] && echo i386
    [[ "$1" == "aarch64" ]] && echo arm64
}
export DEBIAN_FRONTEND=noninteractive
# required
tools_init(){
    if ! which debootstrap &>/dev/null ; then
        wget -c "https://salsa.debian.org/installer-team/debootstrap/-/archive/master/debootstrap-master.zip" -O debootstrap.zip
        unzip debootstrap.zip
        cd debootstrap-master
        make && make install
    fi
}

create_rootfs(){
    run debootstrap --arch=$(get_arch $arch) --no-check-gpg --no-merged-usr --exclude=usrmerge --extractor=ar "$codename" "$rootfs" "$repository"
    run_in_chroot apt install live-boot live-config
}

