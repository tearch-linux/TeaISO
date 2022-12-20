from subprocess import getoutput
from ctypes import CDLL, c_int, c_char_p
from datetime import datetime
import os
import sys
libteaiso = CDLL("libteaiso.so")
libteaiso.run.argtypes = [c_char_p]
libteaiso.run.restype = c_int

libteaiso.get_argument_value.argtypes = [c_char_p, c_char_p]
libteaiso.get_argument_value.restype = c_char_p

libteaiso.colorize.argtypes = [c_char_p, c_char_p]
libteaiso.colorize.restype = c_char_p

libteaiso.set_rootfs.argtypes = [c_char_p]
libteaiso.out.argtypes = [c_char_p]
libteaiso.err.argtypes = [c_char_p]
libteaiso.warn.argtypes = [c_char_p]
libteaiso.inf.argtypes = [c_char_p]

libteaiso.is_root.restype = c_int
simulation = False

VERSION = "2.2.0"

error_event = None

def run(cmd, vital=True):
    if simulation:
        return 0
    cmd = " ".join(str(cmd).split())
    inf("=> Executing: {}".format(colorize(cmd, 0)))
    i = libteaiso.run(cmd.encode("utf-8"))
    if i != 0 and vital:
        err("Failed to run command:{}".format(cmd))
    return i


def err(msg, colorize=True):
    if error_event:
        error_event()
    libteaiso.err(str(msg).encode("utf-8"), now())
    exit(1)


def out(msg, colorize=True):
    libteaiso.out(str(msg).encode("utf-8"), now())


def warn(msg, colorize=True):
    libteaiso.warn(str(msg).encode("utf-8"), now())


def dbg(msg, colorize=True):
    libteaiso.dbg(str(msg).encode("utf-8"), now())


def inf(msg, colorize=True):
    libteaiso.inf(str(msg).encode("utf-8"), now())


def colorize(msg, num):
    return libteaiso.colorize(str(msg).encode("utf-8"), str(num).encode("utf-8")).decode("utf-8")


def set_rootfs(rootfs):
    libteaiso.set_rootfs(rootfs.encode("utf-8"))


def disable_color():
    libteaiso.disable_color()


def is_root():
    return libteaiso.is_root() == 1


def set_error_event(func=None):
    global error_event
    error_event = func

def set_simulation():
    global simulation
    simulation = True


def now():
    return str(datetime.now().strftime("%d/%m/%y %H:%M")).encode("utf-8")


def versiontuple(v):
   filled = []
   for point in str(v).split("."):
      filled.append(point.zfill(8))
   return tuple(filled)

def run_hook(settings, i):
    inf("==> Running: {}".format(colorize(i, 0)))
    run("cat \"{}\" > \"{}/tmp/hook\"".format(settings.profile+"/"+i, settings.rootfs))
    os.chmod("{}/tmp/hook".format(settings.rootfs), 0o755)
    run("chroot \"{}\" bash -e /tmp/hook".format(settings.rootfs))
    run("rm -f \"{}/tmp/hook\"".format(settings.rootfs))


class Args:
    def get_argument_value(self, arg, var):
        return libteaiso.get_argument_value(arg.encode("utf-8"), var.encode("utf-8")).decode("utf-8")

    def get_value(self, i):
        if "=" in i:
            return self.get_argument_value(i, i.split("=")[0])
        elif i.startswith("-"):
            if i in sys.argv:
                n = sys.argv.index(i)
                if n < len(sys.argv):
                    return sys.argv[n+1]
                else:
                    err("Missing argument value {}".format(i))
            else:
                err("Invalid argument {}".format(i))
        else:
            err("Unexcepted argument {}".format(i))

    def is_arg(i, var):
        return i.startswith("--{}".format(var)) or i.startswith("-{}".format(var[0]))

    def help_message():
        disable_color()
        out("""Usage: mkteaiso -p=PROFILE [OPTION]...
ISO generation tool for GNU/Linux, v{}.
Example: mkteaiso -p=/usr/lib/teaiso/profiles/archlinux --interactive
Profile directory should contain profile.yaml.

Base Arguments:
  -p=PROFILE, --profile=PROFILE     Profile directory or name (default: archlinux)
  -o=OUTPUT, --output=OUTPUT        ISO output directory (default: /var/teaiso/output)
  -w=WORK, --work=WORK              ISO work directory (default: /var/teaiso/work)
  -s=SHARED, --shared=SHARED        Shared directory (default: None)
  -c=BASE, --create=BASE            Create profile by base profile
  -g=KEY, --gpg=KEY                 Sign airootfs image by GPG

Miscellaneous:
  -h, --help                        Display this help text and exit
      --version                     Display version and exit
      --nocolor                     Disable colorized output
      --simulate                    Enable simulation mode
      --nocheck                     Skip all check
      --interactive                 Interactive operations
      --debug                       Enable debug mode""".format(VERSION))
        exit(0)
        
    def unrecognized_opt(option):
        out("""mkteaiso: unrecognized option '{}'
Usage: mkteaiso -p=PROFILE [OPTION]...
Try 'mkteaiso --help' for more information.""".format(option))
        exit(2)


class Stage:
    def get(self):
        workdir = os.environ["workdir"]
        if not os.path.exists("{}/stage".format(workdir)):
            self.set(0)

            return 0
        with open("{}/stage".format(workdir), "r") as f:
            return int(f.read())

    def set(self, stage):
        workdir = os.environ["workdir"]
        inf("Stage:{} done.".format(stage))
        with open("{}/stage".format(workdir), "w") as f:
            return f.write(str(stage))


class Mount:
    def mount(rootfs):
        for dir in ["dev", "dev/pts", "sys", "proc", "run"]:
            run("mount --make-private --bind /{1} /{0}/{1} 2>/dev/null".format(rootfs, dir))
        run("ln -s {0}/proc/self/fd {0}/dev/fd 2>/dev/null || true".format(rootfs), vital=False)
        run("ln -s {0}/proc/self/mounts {0}/etc/mtab || true".format(rootfs), vital=False)
        

    def unmount(rootfs):
        for dir in ["dev/pts", "dev", "sys", "proc", "run", "profile"]:
            while 0 == run("umount -lf -R /{}/{}".format(rootfs, dir), vital=False):
                True
