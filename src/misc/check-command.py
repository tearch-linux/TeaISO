#!/usr/bin/python3
import os,sys


missing=[]

def check(cmd):
    if os.system("which "+str(cmd)+" &>/dev/null") != 0:
        missing.append(cmd)

for cmd in ["busybox", "xorriso", "mksquashfs", "dd", "mmd", "grub-mkimage", "grub-editenv",  "find", "ln", "chroot", "cp", "cat", "bash"]:
    check(cmd)
if len(missing) > 0:
    print("Commands are missing:\n"+" ".join(missing),file=sys.stderr)
    sys.exit(1)
