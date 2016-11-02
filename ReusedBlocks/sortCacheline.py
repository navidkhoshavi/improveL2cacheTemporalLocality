import sys
import re
import operator
import os


with open('../llc_access_trace.log', 'r') as fin:
        lines = [line.split() for line in fin]
        lines.sort(key=operator.itemgetter(2))

with open('llc_access_trace_sorted.log', 'w') as fout:
    for el in lines:
        fout.write('{0}\n'.format(' '.join(el)))

