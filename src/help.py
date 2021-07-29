from utils import out as o
from utils import disable_color

def help_message():
    disable_color()
    o("Usage: mkteaiso [options]")
    o("  --output    :    Iso output directory (default /var/teaiso/output)")
    o("  --workdir   :    Working directory (default /var/teaiso/workdir)")
    o("  --profile   :    Profile directory or name (default baseline)")
    o("  --nocolor   :    Disable colorized output")
    o("  --debug     :    Print debug logs")
    o("  --simulate  :    Enable simulation mode. Do nothing")
    o("  --nocheck   :    Skip all check.")
    o("  --help      :    Write help message and exit.")
    exit(0)
