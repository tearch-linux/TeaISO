from subprocess import getoutput
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

libteaiso.is_root.restype = c_int
simulation=False

def run(cmd):
    if simulation:
        return 0;
    inf("=> Executing: {}".format(colorize(str(cmd),0)))
    return libteaiso.run(str(cmd).encode("utf-8"))

def err(msg,colorize=True):
    libteaiso.err(str(msg).encode("utf-8"))
    exit(1)

def out(msg,colorize=True):   
    libteaiso.out(str(msg).encode("utf-8"))

def warn(msg,colorize=True):
    libteaiso.warn(str(msg).encode("utf-8"))
    
def dbg(msg,colorize=True):
    libteaiso.dbg(str(msg).encode("utf-8"))

def inf(msg,colorize=True):
    libteaiso.inf(str(msg).encode("utf-8"))

def get_argument_value(arg,var):
    return libteaiso.get_argument_value(arg.encode("utf-8"),var.encode("utf-8")).decode("utf-8")

def colorize(msg,num):
    return libteaiso.colorize(str(msg).encode("utf-8"),str(num).encode("utf-8")).decode("utf-8")

def set_rootfs(rootfs):
    libteaiso.set_rootfs(rootfs.encode("utf-8"))

def disable_color():
    libteaiso.disable_color()
    
def is_root(): 
    return libteaiso.is_root() == 1

def set_simulation():
    global simulation
    simulation = True
