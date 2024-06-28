# index.py
# Show my [index]

from sys import argv
from icfp.icfp import assemble, eval, post

program = ['STR get index']

icfp = assemble(program)
r = post(icfp)
print(eval(r.text))

