# Send the entry message.

from icfp.icfp import post

r = post("S'%4}).$%8")
with open('problems/test1.icfp', 'w') as f_out:
    f_out.write(r.text)
