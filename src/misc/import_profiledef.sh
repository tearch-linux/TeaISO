declare -A file_permissions=()
source profiledef.sh
echo "name: ${iso_name}"
echo "distro: archlinux"
echo "publisher: ${iso_publisher}"
echo "label: ${iso_label}"
echo "application_id: ${iso_application}"
echo "arch: ${arch}"
echo "pacman: ${pacman_conf}"
echo "packages:"
echo " - packages.x86_64"
echo "grub_cfg: grub.cfg"
echo "airootfs_directory_pre: airootfs"
for dir in ${!file_permissions[@]} ; do
    echo " - $dir|${file_permissions[$dir]}"
done
