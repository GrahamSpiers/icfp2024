# get [service]
#
# Get the index:
#   $python3 cmds/get.py index
# Get the scoreboard:
#   $python3 cmds/get.py scoreboard

from sys import argv
from icfp.icfp import assemble, eval, post

program = [f'STR get {argv[1]}']

icfp = assemble(program)
r = post(icfp)
print(eval(r.text))