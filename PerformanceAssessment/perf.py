#!/usr/bin/python -O
# This code is a modified version of python code written by Mu-Tien Chang

import sys
import re
import os

#python perf.py blackscholes edram_45nm_96MB_mix 8 ooo_l3
benchmark = sys.argv[1] # ex. blackscholes
#tech = sys.argv[2] # e.g., sram_32nm_32MB_mix
num_core = sys.argv[2] # ex. 8
machine = sys.argv[3] # ex. ooo_l3


def system_perf():
    cycle = re.compile("Stopped after ([0-9]+) cycles, ([0-9]+) instructions(.*)")
    refresh = re.compile("Total number of refreshes = ([0-9]+)")

    ipc = 0.0
    num_ins = 0
    num_cycle = 0
    num_refresh = 0
    
    fin1 = open('../'+benchmark + '.log', 'r')
    #fin1 = open(infile1, 'r')

    for line in fin1:
        c = cycle.match(line)
        r = refresh.match(line)

        if c is not None: 
            num_cycle = int(c.group(1))
            num_ins = int(c.group(2))
        if r is not None: 
            num_refresh = int(r.group(1))

    fin1.close()

    ipc = float(num_ins) / num_cycle

    return ipc, num_ins, num_cycle, num_refresh


def cache_perf(cache_object, num_cycle, num_ins):
    start = re.compile("  %s:" %cache_object)
    #read_hit = re.compile("        read: {hit: ([0-9]+), forward: ([0-9]+)}") # my change
    read = re.compile('          read:') # my change    for hit read
    read_hit = re.compile('            hit: ([0-9]+)\n')
    write = re.compile('          write:') # my change    for hit write
    #write_hit = re.compile("        write: {hit: ([0-9]+), forward: ([0-9]+)}") #
    write_hit = re.compile('            hit: ([0-9]+)\n') # my change
    #miss = re.compile("        miss: {read: ([0-9]+), write: ([0-9]+)}")
    miss = re.compile('        miss:') # my change
    read_miss = re.compile('          read: ([0-9]+)\n') # my change
    write_miss = re.compile('          write: ([0-9]+)\n') # my change
    update = re.compile("      update: ([0-9]+)")

    flag = 0
    flag_read_hit = 0
    flag_write_hit = 0
    flag_miss = 0

    num_read = 0
    num_read_hit = 0
    num_read_miss = 0
    read_miss_ratio = 0.0

    num_write = 0
    num_write_hit = 0
    num_write_miss = 0
    write_miss_ratio = 0.0
    
    miss_ratio = 0.0

    num_update = 0 # number of updates from upper caches
    
    num_access = 0
    num_access_per_kins = 0.0
    num_access_per_kcyc = 0.0

    fin2 = open('../'+benchmark+ '_perf.stats', 'r')

    for line in fin2:
        s = start.match(line)
        r_read_hit = read.match(line) # my change
        r = read_hit.match(line)
        w_write_hit = write.match(line)
        w = write_hit.match(line)
        m = miss.match(line)
        m_read = read_miss.match(line)
        m_write = write_miss.match(line)
        u = update.match(line)

        if s is not None: flag = 1
        if flag == 1:
            if r_read_hit is not None: flag_read_hit = 1 # my change
            if w_write_hit is not None: flag_write_hit = 1 # my change
            if m is not None: flag_miss = 1 # my change
        if flag == 1 and flag_read_hit == 1:
            if r is not None: 
                num_read_hit = int(r.group(1))
                flag_read_hit = 0 # my change
        if flag == 1 and flag_write_hit == 1: # my change
            if w is not None: 
                num_write_hit = int(w.group(1))
                flag_write_hit = 0 # my change
        if flag == 1 and flag_miss == 1:
            if m_read is not None:
                num_read_miss = int(m_read.group(1))
            if m_write is not None:
                num_write_miss = int(m_write.group(1))
                flag_miss = 0
                flag = 0
            #if u is not None: 
                #num_update = int(u.group(1))
                #flag = 0   # My change

    fin2.close()

    num_read = num_read_hit + num_read_miss
    num_write = num_write_hit + num_write_miss
    num_insert = num_read_miss + num_write_miss
    if (num_read + num_write)!= 0:
        miss_ratio = float(num_read_miss + num_write_miss) / (num_read + num_write)
    mpki = 1E3 * float(num_read_miss + num_write_miss) / num_ins

    return num_read, num_read_hit, num_read_miss, num_write, num_write_hit, num_write_miss, num_update, num_insert, miss_ratio, mpki


# === main ===
#os.makedirs('my_results')
#os.chdir('my_results')
fout = open('perf.dat', 'w')

# system performance
(ipc, 
 num_ins, 
 num_cycle, 
 num_refresh) = system_perf()

# L1_D performance
L1_D = []
for i in range(int(num_core)):
    L1_D += ['L1_D_%d' %i]

l1_d_num_read = 0
l1_d_num_read_hit = 0
l1_d_num_read_miss = 0
l1_d_num_write = 0
l1_d_num_write_hit = 0
l1_d_num_write_miss = 0
l1_d_num_update = 0
l1_d_num_insert = 0

for l1_d in L1_D:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l1_d, num_cycle, num_ins)

    l1_d_num_read += num_read
    l1_d_num_read_hit += num_read_hit
    l1_d_num_read_miss += num_read_miss
    l1_d_num_write += num_write
    l1_d_num_write_hit += num_write_hit
    l1_d_num_write_miss += num_write_miss
    l1_d_num_update += num_update
    l1_d_num_insert += num_insert

# L1_I performance
L1_I = []
for i in range(int(num_core)):
    L1_I += ['L1_I_%d' %i]

l1_i_num_read = 0
l1_i_num_read_hit = 0
l1_i_num_read_miss = 0
l1_i_num_write = 0
l1_i_num_write_hit = 0
l1_i_num_write_miss = 0
l1_i_num_update = 0
l1_i_num_insert = 0

for l1_i in L1_I:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l1_i, num_cycle, num_ins)

    l1_i_num_read += num_read
    l1_i_num_read_hit += num_read_hit
    l1_i_num_read_miss += num_read_miss
    l1_i_num_write += num_write
    l1_i_num_write_hit += num_write_hit
    l1_i_num_write_miss += num_write_miss
    l1_i_num_update += num_update
    l1_i_num_insert += num_insert

# L2 performance
L2 = []
for i in range(int(num_core)):
    L2 += ['L2_%d' %i]

l2_num_read = 0
l2_num_read_hit = 0
l2_num_read_miss = 0
l2_num_write = 0
l2_num_write_hit = 0
l2_num_write_miss = 0
l2_num_update = 0
l2_num_insert = 0

for l2 in L2:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l2, num_cycle, num_ins)

    l2_num_read += num_read
    l2_num_read_hit += num_read_hit
    l2_num_read_miss += num_read_miss
    l2_num_write += num_write
    l2_num_write_hit += num_write_hit
    l2_num_write_miss += num_write_miss
    l2_num_update += num_update
    l2_num_insert += num_insert

# L3 performance
l3_num_read = 0
l3_num_read_hit = 0
l3_num_read_miss = 0
l3_num_write = 0
l3_num_write_hit = 0
l3_num_write_miss = 0
l3_num_update = 0

if machine == 'ooo_l3' or machine == 'atom_l3':
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf('L3_0', num_cycle, num_ins)

    l3_num_read = num_read
    l3_num_read_hit = num_read_hit
    l3_num_read_miss = num_read_miss
    l3_num_write = num_write
    l3_num_write_hit = num_write_hit
    l3_num_write_miss = num_write_miss
    l3_num_update = num_update
    l3_num_insert = num_insert
    l3_miss_ratio = miss_ratio
    l3_mpki = mpki

else:
    l3_num_read = 0
    l3_num_read_hit = 0
    l3_num_read_miss = 0
    l3_num_write = 0
    l3_num_write_hit = 0
    l3_num_write_miss = 0
    l3_num_update = 0
    l3_num_insert = 0
    l3_miss_ratio = 0
    l3_mpki = 0



# insert results in separate files#
fl1_d = open('L1_d_perf'+'.log', 'w')
print >>fl1_d, "l1_d_num_read=%d l1_d_num_read_hit=%d l1_d_num_read_miss=%d l1_d_num_write=%d l1_d_num_write_hit=%d l1_d_num_write_miss=%d l1_d_num_update=%d l1_d_num_insert=%d \n" %(l1_d_num_read,l1_d_num_read_hit,l1_d_num_read_miss,l1_d_num_write,l1_d_num_write_hit,l1_d_num_write_miss,l1_d_num_update,l1_d_num_insert)
fl1_d.close() 

fl1_i = open('L1_i_perf'+'.log', 'w')
print >>fl1_i, "l1_i_num_read=%d l1_i_num_read_hit=%d l1_i_num_read_miss=%d l1_i_num_write=%d l1_i_num_write_hit=%d l1_i_num_write_miss=%d l1_i_num_update=%d l1_i_num_insert=%d \n" %(l1_i_num_read,l1_i_num_read_hit,l1_i_num_read_miss,l1_i_num_write,l1_i_num_write_hit,l1_i_num_write_miss,l1_i_num_update,l1_i_num_insert)
fl1_i.close()

fl2 = open('L2_perf'+'.log', 'w') 
print >>fl2 , "l2_num_read=%d l2_num_read_hit=%d l2_num_read_miss=%d l2_num_write=%d l2_num_write_hit=%d l2_num_write_miss=%d l2_num_update=%d l2_num_insert=%d \n" %(l2_num_read,l2_num_read_hit,l2_num_read_miss,l2_num_write,l2_num_write_hit,l2_num_write_miss,l2_num_update,l2_num_insert)
fl2.close()

fl3 = open('L3_perf'+'.log', 'w')
print >>fl3, "l3_num_read=%d l3_num_read_hit=%d l3_num_read_miss=%d l3_num_write=%d l3_num_write_hit=%d l3_num_write_miss=%d l3_num_update=%d l3_num_insert=%d num_refresh=%d \n" %(l3_num_read,l3_num_read_hit,l3_num_read_miss,l3_num_write,l3_num_write_hit,l3_num_write_miss,l3_num_update,l3_num_insert,num_refresh)
fl3.close() 
#  End #



# print results
print "IPC=%f MISS_RATIO=%f MPKI=%f" %(ipc, l3_miss_ratio, l3_mpki)

#print >>fout, "IPC=%f num_cycle=%d MISS_RATIO=%f MPKI=%f \n" %(ipc, num_cycle, l3_miss_ratio, l3_mpki),
print >>fout, "%f %d %f %f " %(ipc, num_cycle, l3_miss_ratio, l3_mpki),
print >>fout, "%d %d %d %d %d %d %d %d " %(l1_d_num_read,
                                           l1_d_num_read_hit,
                                           l1_d_num_read_miss,
                                           l1_d_num_write,
                                           l1_d_num_write_hit,
                                           l1_d_num_write_miss,
                                           l1_d_num_update,
                                           l1_d_num_insert),

print >>fout, "%d %d %d %d %d %d %d %d " %(l1_i_num_read,
                                           l1_i_num_read_hit,
                                           l1_i_num_read_miss,
                                           l1_i_num_write,
                                           l1_i_num_write_hit,
                                           l1_i_num_write_miss,
                                           l1_i_num_update,
                                           l1_i_num_insert),

print >>fout, "%d %d %d %d %d %d %d %d " %(l2_num_read,
                                           l2_num_read_hit,
                                           l2_num_read_miss,
                                           l2_num_write,
                                           l2_num_write_hit,
                                           l2_num_write_miss,
                                           l2_num_update,
                                           l2_num_insert),

print >>fout, "%d %d %d %d %d %d %d %d %d" %(l3_num_read,
                                           l3_num_read_hit,
                                           l3_num_read_miss,
                                           l3_num_write,
                                           l3_num_write_hit,
                                           l3_num_write_miss,
                                           l3_num_update,
                                           l3_num_insert,
                                           num_refresh)

fout.close()
