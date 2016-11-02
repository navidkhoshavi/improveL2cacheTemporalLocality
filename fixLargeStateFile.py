#!/usr/bin/python -O


import sys
import re
import os

# python perf.py blackscholes
benchmark = sys.argv[1]  # ex. blackscholes

newfile = open(benchmark + '_perf' + '.stats', "w")
fin1 = open(benchmark + '.stats', 'r')

L_list = ['  L1_I_0:', '  L1_I_1:', '  L1_I_2:', '  L1_I_3:', '  L1_I_4:', '  L1_I_5:', '  L1_I_6:', '  L1_I_7:',
           '  L1_D_0:', '  L1_D_1:', '  L1_D_2:', '  L1_D_3:', '  L1_D_4:', '  L1_D_5:', '  L1_D_6:', '  L1_D_7:', '  L2_0:', '  L2_1:', '  L2_2:', '  L2_3:', '  L2_4:', '  L2_5:', '  L2_6:', '  L2_7:', '  L3_0:','  MEM_0:']

i = 0
line_offset = []
offset = 0
for line in fin1:
    if re.match(L_list[i],line):
        while True:
            if (re.match(L_list[i+1],line)):
                break
            else:
                newfile.write(line)
                line = fin1.next()
                offset += len(line)

        i += 1
        if line == '  MEM_0:\n':
            break
        else:
            # send the cursor to the previous line
            line_offset.append(offset)
            fin1.seek(0)
            fin1.seek(line_offset[i-1])



newfile.close()
fin1.close()

