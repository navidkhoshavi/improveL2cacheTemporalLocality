import sys
import re
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

with open(trace_file, 'rb') as fh:
    first = next(fh)
    offs = -100
    while True:
        fh.seek(offs, 2)
        lines = fh.readlines()
        if len(lines)>1:
            last = lines[-1]
            break
        offs *= 2
    last_line = int(last.split()[0])

i = 1462533
n = 0
k = 0
tmpline = " "

#preSimCycleAccess: first write before the consequence read operations
fout = open(output,"w") 		#CL_access.log
with open(trace_file, 'rb') as ftrace:  #LLC1_sorted.log
    lines = ftrace.readlines()
    while 1:
        #for m in range(0, len(lines)):
            #line = lines[m]
        if n == 0:
            line = lines[i]
        R_counter = 0
        n += 1
        W_counter = 0
        WB_counter = 0
        prevLine = ""
        CL = int(line.split()[2])                # CL: Cache line
        preMemAccess = int(line.split()[1])      #preMemAccess: first memory access to cache line
        while CL == int(line.split()[2]):
            #if (preMemAccess == 1 or preMemAccess == 2 or preMemAccess == 3 or preMemAccess == 4) and int(line.split()[1]) == 0: # compute how many times the memory access is changed to read access
                #avgCoefficient += 1
            if int(line.split()[1]) == 0:
                R_counter += 1
                preMemAccess = int(line.split()[1])
                tmpline = lines[i+1]
                if (int(line.split()[0]) == last_line) or int(tmpline.split()[2]) != CL:
                    break
                line = lines[i+1]
                i += 1
            elif int(line.split()[1]) == 1:
                W_counter += 1
                preMemAccess = int(line.split()[1])
                tmpline = lines[i+1]
                if (int(line.split()[0]) == last_line) or int(tmpline.split()[2]) != CL:   # int(line.split()[2]).lines[i+1]!= CL
                    break
                line = lines[i+1]
                i += 1
            elif int(line.split()[1]) == 2: # write back from L2 to LLC
                WB_counter += 1
                preMemAccess = int(line.split()[1])
                tmpline = lines[i+1]
                if (int(line.split()[0]) == last_line) or int(tmpline.split()[2]) != CL:   # int(line.split()[2]).lines[i+1]!= CL
                    break
                line = lines[i+1]
                i += 1
            else:
                #preSimCycleAccess = int(line.split()[0])
                preMemAccess = int(line.split()[1])
                tmpline = lines[i+1]
                if (int(line.split()[0]) == last_line) or int(tmpline.split()[2]) != CL:
                    break
                line = lines[i+1]
                i += 1

        print >>fout, "%-9s %-9s %-9s %-9s" % (CL, R_counter, W_counter, WB_counter)
        if int(line.split()[0]) != last_line and k < 200000:
            k += 1
            line = lines[i+1]
            i += 1
        else:
            break
fout.close()


# fix me: in the second elsif, I have to consider the previous Mem access
