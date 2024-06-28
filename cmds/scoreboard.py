# [scoreboard] service

from icfp.icfp import assemble, eval, post

program = ['STR get scoreboard']

icfp = assemble(program)
r = post(icfp)
print(eval(r.text))