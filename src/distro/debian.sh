# additional
get_arch(){
    [[ "$1" == "x86_64" ]] && echo amd64
    [[ "$1" == "i686" ]] && echo i386
    [[ "$1" == "aarch64" ]] && echo arm64
}

# required
create_rootfs(){
    run debootstrap --arch=$(get_arch $arch) "$codename" "$rootfs" "$repository"
}

