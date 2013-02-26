#!/usr/bin/env python
# Would have done this in Bash if it wasn't for the convenient 
# settings.py file. 
# Assumes sa-learn is in PATH from cron, incron or settings 
# environment. 

from os import path
from sys import stderr, exit, path as pythonpath
from datetime import datetime
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

    arguments = []
    arguments.append(settings.SA_LEARN)
    if isinstance(args, list):
        arguments.extend(args)
    elif not isinstance(args, str):
        raise TypeError('Must have string or list argument')
    else:
        arguments.extend(args.split())

    try:
        proc = subprocess.Popen(
            arguments,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        (out, err) = proc.communicate()
        rc = proc.returncode
    except(IOError, OSError), e:
        raise
    except(), e:
        raise
    else:
        return (out, err)
    return False

# First do backup
today = datetime.now()
try:
    (out, err) = run_sa_learn('--backup')
except(), e:
    print >>stderr, str(e)
    exit(1)
else:
    backupFilename = '%s/sadb_%s.txt' % (
        settings.SA_DB_BACKUP_DIR,
        today.strftime('%Y-%m-%d.%s')
    )
    try:
        backupFile = open(backupFilename, 'w')
    except(), e:
        print >>stderr, str(e)
        exit(1)
    else:
        backupFile.write(out)
        backupFile.close()

# Run on spam directory
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
