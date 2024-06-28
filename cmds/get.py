# get [service]
#
# Get the index:
#   $python3 cmds/get.py index
# Get the scoreboard:
#   $python3 cmds/get.py scoreboard

from sys import argv
from icfp.icfp import get

print(get(argv[1]))
