# processTweets.py
# crawl the tweets, and look for keywords
# output with daily resolution
#
# NOTES
# uses the new 15-minute compressed format
# 
# USAGE 
# gzip -cd tweets.gz | python processTweet.py 2014-01-01 keywords
#  
# this will read keywords.txt and the tweets from stdin
# and save a frequency file, labMT vector in keywords/[keyword]
# for each keyword

# we'll use most of these
from json import loads,dumps
import codecs
from re import findall,UNICODE
import sys
sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
from labMTsimple.speedy import *
from labMTsimple.storyLab import *
my_LabMT = LabMT(stopVal=0.0)
from os.path import isfile,abspath,isdir
from numpy import zeros,savetxt
from numpy import nonzero
from scipy.sparse import lil_matrix,issparse,csr_matrix
import cPickle as pickle

import glob
from datetime import datetime,timedelta

def add_day(day):
    day_matrix = csr_matrix((10222,10222),dtype="i")

    date = day
    
    output_filename = date.strftime("keywords/%Y-%m-%d.dat")

    nextday = day+timedelta(days=1)

    resolution = timedelta(minutes=15)
    while date < nextday:
        filename = date.strftime("keywords/%Y-%m-%d-%H-%M.dat")
        date+=resolution
        print(filename)
        if not isfile(filename):
            continue
        curr_matrix = pickle.load( open(filename, "rb" ))
            
        # add current matrix to day_matrix (both sparse)
        day_matrix = day_matrix + curr_matrix.tocsr()
        
    pickle.dump(day_matrix.tolil(), open( output_filename, "wb" ) ,pickle.HIGHEST_PROTOCOL)
    
if (__name__ == '__main__'):

    day = datetime.strptime(sys.argv[1],'%Y-%m-%d')
    print(day)
    add_day(day)


