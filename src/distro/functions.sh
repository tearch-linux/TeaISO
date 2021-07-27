run(){
    echo -e "\033[32;1m==> Running:\033[;0m" $@
    $@
}
run_in_chroot(){
    echo -e "\033[32;1m==> Running in chroot:\033[;0m" $@
    chroot "$rootfs" $@
}
