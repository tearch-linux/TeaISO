from utils import out as o
from utils import disable_color

def help_message():
    disable_color()
    o("Usage: mkteaiso [options]")
    o("  -o --output   :    Iso output directory (default /var/teaiso/output)")
    o("  -w --workdir  :    Working directory (default /var/teaiso/workdir)")
    o("  -p --profile  :    Profile directory or name (default baseline)")
    o("     --nocolor  :    Disable colorized output")
    o("  -d --debug    :    Print debug logs")
    o("     --simulate :    Enable simulation mode. Do nothing")
    o("     --nocheck  :    Skip all check.")
    o("  -h --help     :    Write help message and exit.")
    exit(0)
