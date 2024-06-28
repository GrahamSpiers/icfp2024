# [echo] service

from sys import argv
from icfp.icfp import assemble, eval, post


text = ' '.join(argv[1:])

program = ['STR echo '+text]

icfp = assemble(program)
r = post(icfp)
print(eval(r.text))