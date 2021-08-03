from utils import inf, run
def run_hook(settings,i):
    inf("==> Running: {}".format(colorize(i, 0)))
    os.chmod(settings.profile + "/" + i, 0o755)
    run("cat \"{}\" > \"{}/tmp/hook\"".format(settings.profile+"/"+i,settings.rootfs))
    run("chroot \"{}\" /tmp/hook".format(settings.rootfs))
    run("rm -f \"{}/tmp/hook\"".format(settings.rootfs))
