# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import os
import sys
import subprocess
import time

jobs = int(subprocess.check_output("qstat | grep keywordScrapeAdd | wc -l",shell=True))
print(jobs)

max_jobs = 150
jobs_remaining = max_jobs - jobs

loop_counter = 0

batch_size = 1
start = "2008-09-12"
date = datetime.datetime.strptime(start,'%Y-%m-%d')

while jobs_remaining > batch_size and date < datetime.datetime.now():
    date += datetime.timedelta(days=1)

    loop_counter += 1
    print("in the loop, time number {0}".format(loop_counter))

    job='''#PBS -l nodes=1:ppn=1,pmem=8gb,pvmem=9gb
#PBS -l walltime=02:00:00
#PBS -N keywordScrapeAdd
#PBS -j oe

cd /users/a/r/areagan/scratch/2015-11-ambient-bonanza
python3=/users/a/r/areagan/scratch/realtime-parsing/RHEL7-python-3.5.1/bin/python

/usr/bin/time -v $python3 addDaysAndy.py {0}

echo "delete me"'''.format(date.strftime('%Y-%m-%d'))

    if not os.path.isfile(date.strftime('keywords/%Y-%m-%d.pkl')):
        subprocess.call("echo '{0}' | qsub -qshortq".format(job),shell=True)
        time.sleep(0.1)
        
        jobs_remaining -= batch_size
        print("jobs submitted, {0} jobs remaining".format(jobs_remaining))
