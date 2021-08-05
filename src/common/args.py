import sys
from utils import get_argument_value, err


def get_value(i):
    if "=" in i:
        return get_argument_value(i, i.split("=")[0])
    else:
        if i in sys.argv:
            n = sys.argv.index(i)
            if n < len(sys.argv)-1:
                return sys.argv[n+1]
            else:
                err("Missing argument value {}".format(i))
        else:
            err("Invalid argument {}".format(i))


def is_arg(i, var):
    return "--{}".format(var) in i or "-{}".format(var[0]) in i
