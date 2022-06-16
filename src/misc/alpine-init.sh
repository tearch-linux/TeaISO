#!/bin/sh
/bin/busybox --install -s /bin
mount -t devtmpfs devtmpfs /dev
mount -t sysfs sysfs /sys
mount -t proc proc /proc
mount -t tmpfs tmpfs /run
depmod -a
find /lib/modules/$(uname -r) -type f | grep -v debug | sed "s/.*\//modprobe /g;s/\..*//g" | sh 2>/dev/null
mdev -s
live_mount(){
    mkdir -p /alpine/a # upper
    mkdir -p /alpine/b # workdir
    mkdir -p /live_root/
    mkdir -p /new_root/
    mkdir -p /source/ # lower
    mount $root /new_root/ 2> /dev/null
    mount /new_root/live/filesystem.squashfs /source/ 2> /dev/null
    mount -t overlay -o lowerdir=/source/,upperdir=/alpine/a/,workdir=/alpine/b overlay /live_root
    mount -t tmpfs -o size=100% none /alpine/a
    mount -t tmpfs -o size=100% none /alpine/b
    [ -d /source/merge/ ] && cp -prfv /source/merge/* /live_root/
    mount --bind /live_root /new_root/
    mkdir /new_root/cdrom/ 2> /dev/null
    mkdir /new_root/source/ 2> /dev/null
    mount $root /new_root/cdrom/ 2> /dev/null
    mount /new_root/cdrom/live/filesystem.squashfs /new_root/source/ 2> /dev/null
}

is_file_avaiable(){
    disktmp="/tmp/$RANDOM"
    rm -f $disktmp
    mkdir -p $disktmp || true
    timeout 10 mount -t auto "$1" $disktmp &>/dev/null
    [ -f "$disktmp/$2" ] && [ -b "$1" ]
    status=$?
    umount -lf $disktmp 2>/dev/null
    return $status
}

if [ -f /ventoy/hook/arch/ventoy-disk.sh ] ; then
	echo "Loading Ventoy hooks"
	source /ventoy/hook/arch/ventoy-disk.sh &>/dev/null
	sleep 0.3
fi

while [ "$root" == "" ] ; do
	list=$(ls /sys/class/block/ | grep ".*[0-9]$" | grep -v loop | grep -v ram | grep -v nbd | grep -v fd | sed "s|^|/dev/|g")
	for part in $list
	do
		sleep 0.1
		echo "Looking for: $part"
		if is_file_avaiable "$part" "/live/filesystem.squashfs"
		then
			export root=$part
		fi
	done
done
for i in $(cat /proc/cmdline)
do
    echo "export $i" >> /env
done
. /env || true
live_mount
if [ -b /dev/disk/by-label/writable ] ; then
    mount /dev/disk/by-label/writable /new_root/home || true
fi
mount --move /dev /new_root/dev
mount --move /sys /new_root/sys
mount --move /proc /new_root/proc
mount --move /run /new_root/run
if [ "$init" == "" ] ; then
    init=/sbin/init
fi
exec switch_root /new_root $init "$@"
