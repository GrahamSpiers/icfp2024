# Send the entry message.

from icfp.icfp import post

r = post("S'%4}).$%8")
with open('problems/index.icfp', 'w') as f_out:
    f_out.write(r.text)
