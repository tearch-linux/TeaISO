# required
tools_init(){
    if ! which /usr/bin/arch-bootstrap &>/dev/null ; then
        wget -c "https://raw.githubusercontent.com/tokland/arch-bootstrap/master/arch-bootstrap.sh" -O arch-bootstrap.sh
        install arch-bootstrap.sh /usr/bin/arch-bootstrap
    fi
}
create_rootfs(){
    arch-bootstrap -a "$arch" -r "$repository" "$rootfs"
}

