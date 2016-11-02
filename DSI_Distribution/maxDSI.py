import sys
import re


i = 0
maxCLsDSI = 0

#preSimCycleAccess: first write before the consequence read operations
fout = open("maxDSI.log","w")
with open('DSI_new.log', 'r') as ftrace:
    for line in ftrace:
         # the maximum DSI among all CLs
        if maxCLsDSI < int(line.split()[3]):
            maxCLsDSI = int(line.split()[3])

    print >>fout, "%-9s " % (maxCLsDSI)
fout.close()


# fix me: in the second elsif, I have to consider the previous Mem access
