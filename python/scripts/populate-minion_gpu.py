#!/usr/local/bin/python3
from pipeline import stack, pupil, experiment
import logging 
import datajoint as dj

## database logging code 

logging.basicConfig(level=logging.ERROR)
logging.getLogger('datajoint.connection').setLevel(logging.DEBUG)
if hasattr(dj.connection, 'query_log_max_length'):
    dj.connection.query_log_max_length = 3000 

# 3-d segmentation
stack.Segmentation.populate(reserve_jobs=True, suppress_errors=True)

# deeplabcut pupil tracking
next_scans = experiment.AutoProcessing() & (experiment.Scan() & 'scan_ts > "2019-01-01 00:00:00"')
pupil.Tracking.populate(next_scans, {'tracking_method': 2}, reserve_jobs=True,
                        suppress_errors=True)
