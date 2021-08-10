run(){
    echo -e "\033[32;1m==> Running:\033[;0m" $@
    $@
}
run_in_chroot(){
    echo -e "\033[32;1m==> Running in chroot:\033[;0m" $@
    chroot "$rootfs" $@
}
distro_name(){
    name=$(grep "^PRETTY_NAME=" "$rootfs"/etc/os-release | sed "s/^PRETTY_NAME=//g")
    [[ "$name" == "" ]] && name=$(grep "^NAME=" "$rootfs"/etc/os-release | sed "s/^NAME=//g")
    [[ "$name" == "" ]] && name="Unknown"
    echo $name
    
}

generate_sig() {
    if ! [ -z ${gpg+x} ]; then
        for airootfs in $(ls $1/*.squashfs $1/*.sfs $1/*.erofs 2>/dev/null); do
            gpg --pinentry-mode loopback --output $airootfs.sig --detach-sign --default-key "$gpg" $airootfs
        done
    fi
}