import sys
import re

bin0_8M = 0
bin8M_16M = 0
bin16M_32M = 0
bin32M_64M = 0
bin64M_more = 0
fout = open("DSI_dist.log","w")
with open('DSI_new.log', 'r') as ftrace:
    for line in ftrace:
        if int(line.split()[3]) < 8000000:
            bin0_8M += 1
        elif int(line.split()[3]) < 16000000:
            bin8M_16M += 1
        elif int(line.split()[3]) < 32000000:
            bin16M_32M  += 1
        elif int(line.split()[3]) < 64000000:
            bin32M_64M += 1
        else:
            bin64M_more += 1
    print >>fout, "%-9s %-9s %-9s %-9s %-9s" % (bin0_8M, bin8M_16M, bin16M_32M, bin32M_64M, bin64M_more)
fout.close()


# fix me: in the second elsif, I have to consider the previous Mem access
