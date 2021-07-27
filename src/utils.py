import subprocess
from ctypes import CDLL, c_int, c_char_p
libteaiso=CDLL("libteaiso.so")
libteaiso.run.argtypes = [c_char_p]
libteaiso.run.restype=c_int

libteaiso.get_argument_value.argtypes = [c_char_p,c_char_p]
libteaiso.get_argument_value.restype = c_char_p

libteaiso.colorize.argtypes = [c_char_p,c_char_p]
libteaiso.colorize.restype = c_char_p

libteaiso.set_rootfs.argtypes= [c_char_p]
libteaiso.out.argtypes= [c_char_p]
libteaiso.err.argtypes= [c_char_p]
libteaiso.warn.argtypes= [c_char_p]
libteaiso.inf.argtypes= [c_char_p]

libteaiso.restype = c_int

def run(cmd):
    return libteaiso.run(cmd.encode("utf-8"))
def err(msg):   
    libteaiso.err(msg.encode("utf-8"))
    exit(1)

def out(msg,colorize=True):   
    libteaiso.out(msg.encode("utf-8"))

def warn(msg,colorize=True):
    libteaiso.err(warn.encode("utf-8"))

def inf(msg,colorize=True):
    libteaiso.inf(msg.encode("utf-8"))

def get_argument_value(arg,var):
    return libteaiso.get_argument_value(arg.encode("utf-8"),var.encode("utf-8")).decode("utf-8")

def colorize(msg,num):
    return libteaiso.colorize(msg.encode("utf-8"),str(num).encode("utf-8")).decode("utf-8")

def set_rootfs(rootfs):
    libteaiso.set_rootfs(rootfs.encode("utf-8"))

def is_root():
    libteaiso.is_root() == 1
