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
import datetime
from re import findall,UNICODE
import sys
sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
from labMTsimple.speedy import *
from labMTsimple.storyLab import *
my_LabMT = LabMT(stopVal=0.0)

from numpy import zeros,savetxt
from numpy import nonzero
from scipy.sparse import lil_matrix, issparse, csr_matrix
import pickle

def tweetreader(tweettext, my_result):
    # takes in the hashtag-stripped text
    # the keyword list
    # and the title of the file to append to
    
    # for keyword in keywords:
    #     if keyword["re"].search(tweet["text"]) is not None:
    #         # print("match for {0}:".format(keyword["folder"]))
    #         # print(tweet["text"])
    #         g = codecs.open("raw-tweets/{0}/{1}.txt".format(keyword["folder"],outfile),"a","utf8")
    #         g.write(dumps(tweet))
    #         g.write("\n")
    #         g.close()
    #     # else:
    #         # print("no match for {0}".format(keyword["folder"]))

    # with 10000 keywords, better to iterate the other way around

    replaceStrings = ["---","--","''"]
    for replaceString in replaceStrings:
        tweettext = tweettext.replace(replaceString," ")
    tweetwords = [x.lower() for x in findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",tweettext,flags=UNICODE)]
    tweetdict = dict()
    for word in tweetwords:
        if word in tweetdict:
            tweetdict[word] += 1
        else:
            tweetdict[word] = 1
    tweet_wordvec = my_LabMT.wordVecify(tweetdict)
    # if sum(tweet_wordvec) > 0:
    #     for i in range(len(tweet_wordvec)):
    #         if tweet_wordvec[i] > 0:
    #             my_result[i,:] += tweet_wordvec
    # (of course, could vectorize further)
    # simple operations are fast
    # for i in nonzero(tweet_wordvec)[0]:
    #     my_result[i,:] += tweet_wordvec
    # my_result[nonzero(tweet_wordvec)[0],:] += tweet_wordvec
    my_result[(tweet_wordvec > 0),:] += tweet_wordvec
    # print(".")

def gzipper(my_result):
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
            if "text" in tweet:
                # print("found text")
                # print(".", end="")
                tweetreader(tweet["text"], my_result)
            elif "body" in tweet:
                tweetreader(tweet["body"], my_result)
        except:
            print("failed to load a tweet")

def makefolders():
    from os import mkdir
    for a in keywords:
        mkdir("raw-tweets/"+a["folder"])

if __name__ == "__main__":
    keywords = my_LabMT.wordlist
    # my_result = zeros((len(keywords),len(keywords)))
    # my_result = csr_matrix((len(keywords),len(keywords)), dtype='i')
    my_result = lil_matrix((len(keywords),len(keywords)), dtype='i')

    # load the things
    outfile = sys.argv[1]

    gzipper(my_result)

    print("saving...")

    # if not issparse(my_result):
    #     my_result = lil_matrix(my_result,dtype="i")

    f = open(outfile,"wb")
    pickle.dump(my_result, f)
    f.close()
    # savetxt(outfile,my_result,fmt="%.0f",delimiter=",")
    
    print("complete")

    # makefolders()

  








