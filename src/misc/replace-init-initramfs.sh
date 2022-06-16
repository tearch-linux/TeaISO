#!/bin/bash
extract(){
    mkdir -p /tmp/initrd/$(basename $1)
    cat "$1" | gzip -d -f - | cpio -i
}

compress(){
    cd /tmp/initrd/$(basename $1)
    find . | cpio -o -c -R root:root | gzip -9 > /boot/$(basename $1).new
}

add_modules(){
    # See: https://gitlab.com/sulinos/devel/initrd/-/blob/master/src/addons/00-modules.sh#L12
    cp -prf ${MODDIR}/kernel/{crypto,fs,lib,block} ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/input/{keyboard,serio} ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/{ata,md,mmc,firewire} ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/{scsi,pcmcia,virtio} ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/usb/ ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/acpi/ ${WORKDIR}/${MODDIR} || true
	cp -prf ${MODDIR}/kernel/drivers/{block,cdrom}/ ${WORKDIR}/${MODDIR} || true
    find ${WORKDIR}/${MODDIR} -type f | grep "xz$" | xargs xz -d || true
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
    # Remove modules and install better one again.
    echo "Insert kernel modules"
    export MODDIR=/lib/modules/$(echo $file | sed "s/.*initramfs-//g;s/.img//g")
    export WORKDIR=$(pwd)
    rm -rf ${WORKDIR}/${MODDIR} ; mkdir -p ${WORKDIR}/${MODDIR}
    add_modules
    echo "Compress: $file"
    compress $file
    rm -f "$file"
    mv "$file.new" "$file"
done
