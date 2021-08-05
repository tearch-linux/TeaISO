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
