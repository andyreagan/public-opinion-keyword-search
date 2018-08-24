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
import pandas as pd
import glob
import datetime
import click

def extract_day(date, keyword: str) -> pd.DataFrame:
    filename = date.strftime("keywords/%Y-%m-%d.pkl")
    if isfile(filename):
        curr_matrix = pickle.load(gzip.open(filename, "rb"))
        i = my_LabMT.data[keyword][0]
        d = {k: curr_matrix[i,v[0]] for k,v in my_LabMT.data.items()}
        date_str = date.strftime("%Y-%m-%d")
        return pd.DataFrame(d,index=[date_str])
    else:
        print("missing",filename)
        return pd.DataFrame()

@click.command()
@click.argument("keyword")
def main(keyword):
    start = "2008-09-12"
    date = datetime.date(2008,9,13)

    all_days = []
    while date < datetime.date.today():
        if date.day == 1:
            print(date.strftime("%Y-%m-%d"))
        all_days.append(extract_day(date, keyword))
        date += datetime.timedelta(days=1)
    df = pd.concat(all_days)
    df.to_pickle(keyword+".pkl.gz")
    
if __name__ == '__main__':
    main()

