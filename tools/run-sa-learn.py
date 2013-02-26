#!/usr/bin/env python
# Would have done this in Bash if it wasn't for the convenient 
# settings.py file. 
# Assumes sa-learn is in PATH from cron, incron or settings 
# environment. 

from os import path
from sys import stderr, exit, path as pythonpath
import subprocess
import traceback

# Import settings
parentdir = path.dirname(path.dirname(path.abspath(__file__)))
pythonpath.insert(0,parentdir)

import settings

# Wrapper to run sa-learn
def run_sa_learn(args=None):
    if not args:
        raise ValueError('Must have argument')

    if isinstance(args, list):
        arguments = ' '.join(args)
    elif not isinstance(args, str):
        raise TypeError('Must have string or list argument')

    try:
        proc = subprocess.Popen('%s %s' % (settings.SA_LEARN, args))
        (out, err) = proc.communicate()
        rc = proc.returncode
    except(IOError, OSError), e:
        raise
    except(), e:
        raise

# First run on spam directory
try:
    run_sa_learn('--spam %s' % settings.SPAM_DIR)
except(), e:
    print >>stderr, str(e)
    exit(1)

# Then ham dir
try: 
    run_sa_learn('--ham %s' % settings.HAM_DIR)
except(), e:
    print >>stderr, str(e)
    exit(1)
exit(0)
