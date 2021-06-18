import os, sys, shutil, logging
work_directory = None
airootfs_directory = None
   
def make_pkg_conf():
    target_pacman_conf = os.path.realpath(work_directory + "/pacman.conf")
    file = shutil.copyfile(iso_profile["pacman_directory"], target_pacman_conf)

    os.chmod(target_pacman_conf, 0o775)
    
    logging.info("pacman.conf generated successfully!")
    change_status("make_pacman_conf")


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
    packages = run_chroot("pacman -Qqn", work_directory + "/" + "packages.list")
    
    logging.info("Pkglist generated!")
    change_status("make_pkglist")


def install_packages():
    pacman_conf_directory = work_directory + '/' + "pacman.conf"
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    packages = 'base mkinitcpio linux grub '

    for s in iso_profile["all_packages"]:
        packages += s + ' '

    if cmd_line.verbose:
        command = "pacstrap -C {} -c -i -G -M -- {} {}".format(pacman_conf_directory, airootfs_directory, packages)
    else:
        command = "pacstrap -C {} -c -G -M -- {} {} &> /dev/null".format(pacman_conf_directory, airootfs_directory, packages)

    execute_command(command)
    
    logging.info("Packages installed to airootfs!")
    change_status("install_packages")


def make_isowork():
    airootfs_directory = work_directory + '/' + iso_profile["arch"]
    execute_command("du -sb {} | cut -f1 > {}/isowork/live/airootfs.size".format(airootfs_directory, work_directory))
    
    shutil.copyfile(iso_profile["grub_cfg"], work_directory + "/isowork/boot/grub/grub.cfg")
    
    execute_command("md5sum {0}/live/airootfs.sfs > {0}/live/airootfs.md5sum".format(work_directory+"/isowork/"))
    shutil.copy(work_directory + "/" + "packages.list", work_directory + "/isowork")
    
    logging.info("Isowork generated!")
    change_status("make_isowork")