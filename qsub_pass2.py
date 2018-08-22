# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import os
import time

jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print(jobs)

max_jobs = 500
# max_jobs = 150
jobs_remaining = max_jobs - jobs
print(jobs_remaining)

loop_counter = 0

batch_size = 1

end = datetime.datetime(2018,7,24)
end = datetime.datetime.now()
start = datetime.datetime(2018,7,13)
curr = start
dt = datetime.timedelta(minutes=15)
while curr < end and jobs_remaining > batch_size:
    f = curr.strftime("%Y-%m-%d/%Y-%m-%d-%H-%M")
    if not os.path.isfile("keywords/"+f+".pkl"):
        job='''#PBS -l nodes=1:ppn=1
#PBS -l walltime=30:00:00
#PBS -N keywordScrape
#PBS -j oe

cd /users/a/r/areagan/scratch/2015-11-ambient-bonanza

echo "processing {0}"
python3=/users/a/r/areagan/scratch/realtime-parsing/RHEL7-python-3.5.1/bin/python
/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}.gz | $python3 processTweets.py "keywords/{0}.pkl"

echo "delete me"'''.format(f)

        # subprocess.call("echo '{0}' | qsub -qshortq".format(job),shell=True)
        subprocess.call("echo '{0}' | qsub".format(job),shell=True)
        time.sleep(0.1)
        
        jobs_remaining -= batch_size
        print("jobs submitted, {0} jobs remaining".format(jobs_remaining))
    curr += dt
