#!/usr/bin/env python

import glob
import os
import numpy as np
import logging
from make_nptabel_summary import extract_all_beams, find_sources, make_nptable_csv
import csv

# -------------------------------------------------
beams_1 = '/data/apertif/190602049/'
obs_id = '190602049'
module = 'preflag'
#source = 'LH_GRG'

# -----------------------
# to extract a dictionary

beam_info = extract_all_beams(obs_id, module)
print(beam_info[1]['beam'])
print(len(beam_info))

# print(beam_info)

# ------------------------
# to extract a csv file

make_nptable_csv(obs_id, module)
