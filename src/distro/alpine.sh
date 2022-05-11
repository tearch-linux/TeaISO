# additional
write_repo(){
    if [[ "$repository" != "" ]] ; then
        echo "-r $repository"
    fi
}

# required
tools_init(){
    which apk &>/dev/null && return 0
    mkdir -p /tmp/apk
    cd /tmp/apk
    arch="$(uname -m)"
    apktools=$(wget -O - https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/$arch/ | grep "apk-tools-static" | sed "s/^.*=\"//g;s/\".*//g")
    wget -c "https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/$arch/$apktools" -O apk-tools-static.apk
    tar -zxf apk-tools-static.apk
    cp -pf sbin/apk.static /bin/apk
    chmod +x /bin/apk
}
create_rootfs(){
    ls ${DESTDIR}/etc/alpine-release &>/dev/null && return 0
    arch="$(uname -m)"
    REPO="http://dl-cdn.alpinelinux.org/alpine/latest-stable/"
    apk --arch $arch -X "$(write_repo)/main/" -U --allow-untrusted --root "$rootfs" --initdb add alpine-base
    sync
    echo "$(write_repo)/main/" > "$rootfs"/etc/apk/repositories
    echo "$(write_repo)/community/" >> "$rootfs"/etc/apk/repositories
}

populate_rootfs(){
    run_in_chroot apk add linux-edge bash ca-certificates
}

install_packages(){
    run_in_chroot apk add ${packages[@]}
}

make_pkglist() {
    run_in_chroot apk list >  ${workdir}/packages.list
}
