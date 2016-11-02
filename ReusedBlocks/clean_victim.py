import sys
import re
import os
from inspect import currentframe


# access type = 0 = read
# access type = 1 = write
# access type = 2 = update
# access type = 3 = evict
# access type = 4 = prefetch
# access type = 5 = insert (MEM writes LLC) when LLC has a read miss
# access type = 6 = writeback (LLC writes MEM)



trace_file =sys.argv[1]
output = sys.argv[2]

#preSimCycleAccess: first write before the consequence read operations
fout = open(output,"w") #clean_victim.log
cv_8 = 0 # clean victim evicted from L2 less than 8 times
cv_16 = 0
cv_32 = 0
cv_64 = 0
IRRA = 0
clean_victim = 0
with open(trace_file, 'rb') as ftrace: #CL_access.log
    for line in ftrace: 	    	
    	#CL = int(line.split()[2])
    	if int(line.split()[2]) == 0 and int(line.split()[3])==0:
            if int(line.split()[1]) < 8:
                cv_8 +=1
            elif int(line.split()[1]) < 16:
                cv_16 +=1
            elif int(line.split()[1]) < 32:
                cv_32 +=1
            elif int(line.split()[1]) < 64:
                cv_64 +=1
            elif int(line.split()[1]) > 64:
                IRRA +=1
            clean_victim += 1


print >>fout, "%-9s %-9s %-9s %-9s %-9s %-9s" % (cv_8, cv_16, cv_32, cv_64, IRRA, clean_victim)


fout.close()



