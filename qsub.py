# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time

jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print(jobs)

max_jobs = 150
jobs_remaining = max_jobs - jobs

loop_counter = 0

batch_size = 24

while jobs_remaining > batch_size:
    f = open('currdate.txt','r')
    tmp = f.read().rstrip()
    f.close()

    date = datetime.datetime.strptime(tmp,'%Y-%m-%d')
    date += datetime.timedelta(days=1)

    if date > datetime.datetime.now():
    # if date > datetime.datetime(2013,5,27):
        print('date past search range')
        break
    
    loop_counter += 1
    print("in the loop, time number {0}".format(loop_counter))
    f = open('currdate.txt','w')
    tmp = f.write(date.strftime('%Y-%m-%d'))
    f.close()

    for hour in range(24):
        job='''#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00
#PBS -N keywordScrape
#PBS -j oe

cd /users/a/r/areagan/scratch/2015-11-ambient-bonanza

echo "processing {0}-{1:02d}"
/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-{1:02d}-00.gz | python processTweets.py "keywords/{0}-{1:02d}-00.dat"
/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-{1:02d}-15.gz | python processTweets.py "keywords/{0}-{1:02d}-15.dat"
/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-{1:02d}-30.gz | python processTweets.py "keywords/{0}-{1:02d}-30.dat"
/usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-{1:02d}-45.gz | python processTweets.py "keywords/{0}-{1:02d}-45.dat"

echo "delete me"'''.format(date.strftime('%Y-%m-%d'),hour)

        subprocess.call("echo '{0}' | qsub -qshortq".format(job),shell=True)
        time.sleep(0.1)
        
    jobs_remaining -= batch_size
    print("jobs submitted, {0} jobs remaining".format(jobs_remaining))
