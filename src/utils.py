import os
import sys
import shutil
import logging
import glob
logfile="/var/log/teaiso.log"
if os.getuid() != 0:
	logfile=os.environ["HOME"]+"/.local/teaiso.log"
logging.basicConfig(handlers=[logging.FileHandler(logfile), logging.StreamHandler()],
                    format='%(asctime)s [mkteaiso] %(levelname)s: %(message)s', datefmt='%d/%m/%y %H:%M:%S')

def execute_command(command, vital=True):
    process = os.system(command)
    if vital and process != 0:
        logging.error("-> " + command)
        logging.error("Process exited with {}".format(str(process)))
        sys.exit(process)
    return process


def run_chroot(work_directory, iso_profile, command, path="/dev/stdout", vital=True):
    command = command.replace('"', "'").strip()
    target = work_directory + '/' + iso_profile["arch"]
    return execute_command('chroot {} /bin/sh -c "{}" > {}'.format(target, command, path), vital)


def remove_all_contents(directory):
    for path in glob.glob(directory):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def change_status(work_directory, name):
    open(work_directory + "/" + name, 'a').close()


def check_status(work_directory, name):
    if os.path.exists(work_directory):
        if not name in os.listdir(work_directory + "/"):
            return 1
    else:
        return 1


def mount_operations(target, type="mount"):
    if type == "mount":
        for dir in ["dev", "sys", "proc", "run", "dev/pts"]:
            execute_command("mount --bind /{0} {1}/{0}".format(dir, target))
    elif type == "umount":
        for dir in ["dev", "sys", "proc", "run", "dev/pts"]:
            while 0 == os.system("umount -lf -R {1}/{0}".format(dir, target)):
                True
    else:
        logging.error("Please select true type for mount operations!")
        sys.exit(1)

def sign_rootfs(input, cmd_line):
    if cmd_line.gpg:
        execute_command("gpg --output {0}.sig --detach-sign --default-key \"{1}\" {0}".format(input, cmd_line.gpg))