#!/bin/bash
python divide_conquer.py
python sortCacheline.py
python CL_access.py LLC1_sorted.log CL_access.log
python CL_access.py LLC_divide/LLC2_sorted.log LLC_divide/CL2_access.log
python CL_access.py LLC_divide/LLC3_sorted.log LLC_divide/CL3_access.log
python CL_access.py LLC_divide/LLC4_sorted.log LLC_divide/CL4_access.log
python CL_access.py LLC_divide/LLC5_sorted.log LLC_divide/CL5_access.log
python CL_access.py LLC_divide/LLC6_sorted.log LLC_divide/CL6_access.log
python CL_access.py LLC_divide/LLC7_sorted.log LLC_divide/CL7_access.log
python CL_access.py LLC_divide/LLC8_sorted.log LLC_divide/CL8_access.log
python CL_access.py LLC_divide/LLC9_sorted.log LLC_divide/CL9_access.log
python CL_access.py LLC_divide/LLC10_sorted.log LLC_divide/CL10_access.log
python clean_victim.py CL_access.log clean_victim.log
python clean_victim.py LLC_divide/CL2_access.log LLC_divide/clean_victim2.log
python clean_victim.py LLC_divide/CL3_access.log LLC_divide/clean_victim3.log
python clean_victim.py LLC_divide/CL4_access.log LLC_divide/clean_victim4.log
python clean_victim.py LLC_divide/CL5_access.log LLC_divide/clean_victim5.log
python clean_victim.py LLC_divide/CL6_access.log LLC_divide/clean_victim6.log
python clean_victim.py LLC_divide/CL7_access.log LLC_divide/clean_victim7.log
python clean_victim.py LLC_divide/CL8_access.log LLC_divide/clean_victim8.log
python clean_victim.py LLC_divide/CL9_access.log LLC_divide/clean_victim9.log
python clean_victim.py LLC_divide/CL10_access.log LLC_divide/clean_victim10.log
python total_clean_victim.py
