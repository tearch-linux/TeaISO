#!/bin/bash
# This script revoke usrmerge.
set +e
apt-get install busybox-static -yq || exit 1
cp /bin/busybox /busybox
[[ -d /var/lib/dpkg/info/ ]] || exit 1

for dir in lib bin sbin lib32 lib64 libx32 ; do
    /busybox rm -f /$dir && /busybox mkdir /$dir
    /busybox  cat /var/lib/dpkg/info/*.list | /busybox grep "^/$dir" | while read line ; do
        nd="$(/busybox dirname $line)"
        [[ ! -d "$nd" ]] && /busybox mkdir -p "$nd"
        [[ ! -d "/usr/$line" ]] && /busybox mv /usr/$line $line
    done
done
/busybox rm -f  /busybox
