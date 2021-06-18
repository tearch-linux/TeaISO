import os, sys, shutil, logging
work_directory = None
airootfs_directory = None

def make_pkg_conf():
    airootfs_directory = work_directory + '/' + iso_profile["arch"]   
    execute_command('debootstrap --no-merged-usr stable '+airootfs_directory)
    logging.info("apt.conf generated successfully!")
    change_status("make_apt_conf")


def change_status(name):
    open(work_directory + "/" + name, 'a').close()


def execute_command(command,vital=True):
    process = os.system(command)
    if vital and process!=0:
        logging.error("-> "+command)
        logging.error("Process exited with {}".format(str(process)))
        sys.exit(process)
    return process


def run_chroot(command, path="/dev/stdout",vital=True):
    command = command.replace('"', "'").strip()
    target = work_directory + '/' + iso_profile["arch"]
    
    return execute_command('chroot {} /bin/sh -c "{}" > {}'.format(target, command, path),vital)

def make_pkglist():
    packages = run_chroot("apt list --installed ", work_directory + "/" + "packages.list")
    
    logging.info("Pkglist generated!")
    change_status("make_pkglist")



def install_packages():
    pacman_conf_directory = work_directory + '/' + "pacman.conf"
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    packages = 'live-boot live-config initramfs-tools grub-pc-bin grub-efi grub-efi-ia32-bin '

    for s in iso_profile["all_packages"]:
        packages += s + ' '

    command = "chroot {} apt install -yq {}".format(airootfs_directory, packages)
    execute_command(command)
    
    logging.info("Packages installed to airootfs!")
    change_status("install_packages")


def make_isowork():
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    execute_command("du -sb {} | cut -f1 > {}/isowork/live/filesystem.size".format(airootfs_directory, work_directory))
    
    shutil.copyfile(iso_profile["grub_cfg"], work_directory + "/isowork/boot/grub/grub.cfg")
    if os.path.exists("{0}/live/airootfs.sfs".format(work_directory+"/isowork/")):
        execute_command("mv {0}/live/airootfs.sfs {0}/live/filesystem.squashfs".format(work_directory+"/isowork/"))
    execute_command("md5sum {0}/live/filesystem.squashfs > {0}/live/filesystem.md5sum".format(work_directory+"/isowork/"))
    shutil.copy(work_directory + "/" + "packages.list", work_directory + "/isowork")
    
    logging.info("Isowork generated!")
    change_status("make_isowork")