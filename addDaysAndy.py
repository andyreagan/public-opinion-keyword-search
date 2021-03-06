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
# sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
# from labMTsimple.speedy import *
# from labMTsimple.storyLab import *
# my_LabMT = LabMT(stopVal=0.0)
import sys
sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
from labMTsimple.speedy import *
from labMTsimple.storyLab import *
my_LabMT = LabMT(stopVal=0.0)
my_LabMT.data["opioid"] = [len(my_LabMT.data)]
my_LabMT.data["opioids"] = [len(my_LabMT.data)]
import os
from os.path import isfile,abspath,isdir
from numpy import zeros,savetxt
from numpy import nonzero
from scipy.sparse import lil_matrix,issparse,csr_matrix
# import cPickle as pickle
import pickle
from subprocess import call
import gzip

import glob
from datetime import datetime,timedelta

def add_day(day):
    day_matrix = csr_matrix((len(my_LabMT.data),len(my_LabMT.data)),dtype="i")

    date = day
    
    output_filename = date.strftime("keywords/%Y-%m-%d.pkl")

    nextday = day+timedelta(days=1)

    resolution = timedelta(minutes=15)
    while date < nextday:
        filename = date.strftime("keywords/%Y-%m-%d/%Y-%m-%d-%H-%M.pkl")
        date+=resolution
        print(filename)
        if not isfile(filename):
            continue
        try:
            curr_matrix = pickle.load(gzip.open(filename, "rb"))
        except EOFError:
            with open("EOF-errors.txt","a") as f:
                f.write(filename)
                f.write("\n")
            continue
            os.remove(filename)
        except:
            with open("other-errors.txt","a") as f:
                f.write(filename)
                f.write("\n")
            os.remove(filename)
            continue
            
        # add current matrix to day_matrix (both sparse)
        day_matrix = day_matrix + curr_matrix.tocsr()
        
    pickle.dump(day_matrix.tolil(), gzip.open( output_filename, "wb"), pickle.HIGHEST_PROTOCOL)
    
def zip_day(day):
    call("zip keywords/{0}.zip keywords/{0}-*".format(day.strftime("%Y-%m-%d")),shell=True)
    call("lz4 -9f keywords/{0}.dat keywords/{0}.lz4".format(day.strftime("%Y-%m-%d")),shell=True)
    call("\\rm keywords/{0}*.dat".format(day.strftime("%Y-%m-%d")),shell=True)

def unzip_day(day):
    call("unzip keywords/{0}.zip".format(day.strftime("%Y-%m-%d")),shell=True)
    
if (__name__ == '__main__'):

    day = datetime.strptime(sys.argv[1],'%Y-%m-%d')
    print(day)
    # if isfile("keywords/{0}.zip".format(day.strftime("%Y-%m-%d"))):
    #     unzip_day(day)
    add_day(day)
    # zip_day(day)


