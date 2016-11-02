#!/usr/bin/python -O

import sys
import shutil
import os
benchmark = sys.argv[1] # e.g., canneal
tech = sys.argv[2] # e.g., sram_32nm_32MB_mix
# python frq_R.py blackscholes edram_45nm_96MB_mix
if __name__ == "__main__":
	root_directory = os.getcwd()
	os.chdir(root_directory+ "/reuse_rows/post_process/")
	os.system('python post_process.py %s' %benchmark)
	os.chdir(root_directory+ "/reuse_rows/frequently_read/")
	os.system('python frq_R_0WU.py %s %s' %(benchmark, tech))
	os.system('python frq_R.py %s %s' %(benchmark, tech))
	os.system('python mem_op.py %s' %benchmark)
	os.system('python mem_op_0WU.py %s' %benchmark)
	os.chdir(root_directory+ "/RWUE/")
	os.system('python read_AP.py %s %s' %(benchmark, tech))
	os.system('python write_AP.py %s %s' %(benchmark, tech))
	os.system('python update_AP.py %s %s' %(benchmark, tech))
	os.system('python evict_AP.py %s %s' %(benchmark, tech))
