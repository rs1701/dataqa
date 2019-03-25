"""
Script to automatically run crosscal plots
Requires a scan number
Optionally takes a directory for writing plots
"""

import os
from selfcal import selfcal_plots as scplots
import argparse
from timeit import default_timer as timer
from dataqa.scandata import get_default_imagepath
from dataqa.selfcal.selfcal_maps import get_selfcal_maps
from dataqa.selfcal.selfcal_report import get_selfcal_report
import time
from apercal.libs import lib
import logging

start = timer()

parser = argparse.ArgumentParser(description='Generate selfcal QA plots')

# 1st argument: File name
parser.add_argument("scan", help='Scan of target field')
parser.add_argument("target", help='Target name')

parser.add_argument('-p', '--path', default=None,
                    help='Destination for images')

parser.add_argument('--no_report', action="store_true", default=False,
                    help='Disable certain reading the selfcal report')

parser.add_argument('--no_selfcal_maps', action="store_true", default=False,
                    help='Disable certain reading the selfcal report')

parser.add_argument('--no_gain_plots', action="store_true", default=False,
                    help='Disable certain reading the selfcal report')

args = parser.parse_args()

# If no path is given change to default QA path
if args.path is None:
    output_path = get_default_imagepath(args.scan)

    # check that selfcal qa directory exists
    output_path = "{0:s}selfcal/".format(output_path)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
else:
    output_path = args.path

# Create log file
lib.setup_logger(
    'debug', logfile='{0:s}run_scal_plots.log'.format(output_path))
logger = logging.getLogger(__name__)

# Get selfcal maps
if not args.no_report:
    try:
        logger.info("#### Generate selfcal report ...")
        start_time_maps = time.time()
        get_selfcal_report(args.scan, target, output_path)
        logger.info("#### Generate selfcal report. Done ({0:.0f}s)".format(
            time.time()-start_time_maps))
    except Exception as e:
        logger.error(e)
        logger.error("#### Creating selfcal maps failed")
else:
    logger.warning("#### Selfcal report will not be generated")

# Get selfcal maps
if not args.no_selfcal_maps:
    try:
        logger.info("#### Creating selfcal maps ...")
        start_time_maps = time.time()
        get_selfcal_maps(args.scan, output_path)
        logger.info("#### Creating selfcal maps. Done ({0:.0f}s)".format(
            time.time()-start_time_maps))
    except Exception as e:
        logger.error(e)
        logger.error("#### Creating selfcal maps failed")
else:
    logger.warning("#### Selfcal maps will not be generated")

# Get phase plots
if not args.no_gain_plots:
    try:
        logger.info("#### Creating phase plots")
        start_time_plots = time.time()
        PH = scplots.PHSols(args.scan, args.target)
        PH.get_data()
        PH.plot_phase(imagepath=output_path)
        logger.info('#### Done with phase plots ({0:.0f}s)'.format(
            time.time()-start_time_plots))
    except Exception as e:
        logger.error(e)
        logger.error("Creating phase plots failed.")
else:
    logger.warning("#### Selfcal gain plots will not be generated")

# Get amp plots
#AMP = scplots.AMPSols(args.scan, args.target)
# AMP.get_data()
# AMP.plot_amp(imagepath=output_path)

# print 'Done with amplitude plots'


#end = timer()
# print 'Elapsed time to generate cross-calibration data QA inpection plots is {} minutes'.format(
#    (end - start)/60.)
#time in minutes
