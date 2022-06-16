#!/bin/bash
extract(){
    mkdir -p /tmp/initrd/$(basename $1)
    cat "$1" | gzip -d -f - | cpio -i
}

compress(){
    cd /tmp/initrd/$(basename $1)
    find . | cpio -v -o -c -R root:root | gzip -9 > /boot/$(basename $1).new
}

rm -rf /tmp/initrd || true
mkdir -p /tmp/initrd
for file in /boot/initramfs-*.img ; do
    mkdir -p /tmp/initrd/$(basename $file)
    cd /tmp/initrd/$(basename $file)
    echo "Extract: $file"
    extract $file
    rm -f init
    cat "$1" > init
    chmod +x init
    echo "Add busybox binary"
    install /lib/ld-musl-x86_64.so.1 ./lib/ld-musl-x86_64.so.1
    install /usr/sbin/busybox ./bin/busybox
    echo "Compress: $file"
    compress $file
    rm -f "$file"
    mv "$file.new" "$file"
done
