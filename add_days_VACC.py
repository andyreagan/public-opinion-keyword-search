import cPickle as pickle
import glob
import scipy.sparse
from datetime import date, timedelta as td
import sys,os

def add_day(day):

    path = "/users/a/r/areagan/fun/twitter/keyword-searches/2015-11-ambient-bonanza/keywords/"
    path2 = "/users/e/m/emcody/ambient_happ/"
    
    #path = '../desktop/ambient_happ/'
    #path2 = '../desktop/ambient_happ/'
    
    #intialize dictionary by day
    #dict_by_day = {}
    
    #intialize day matrix
    day_matrix = scipy.sparse.csr_matrix((10222,10222))
        
##################### loop over 15 min intervals in 1 day ######################
    #1 day takes ~15 mins 
    for filename in glob.glob(path+day+"*.dat"):
        print(filename)
            
        #10,222x10,222 
        #Keyword x otherWords
        curr_matrix = pickle.load( open(filename, "rb" ))
            
        #add current matrix to day_matrix (both sparse)
        day_matrix = day_matrix + curr_matrix.tocsr()
        
    #save to dictionary    
    #dict_by_day[day] = day_matrix
        
    #save to file 
    pickle.dump(day_matrix.to_lil(), open( path2+day+".dat", "wb" ) )
    
if (__name__ == '__main__'):

#    if (len(sys.argv) != 2):
#       print 'usage: python topics.py <day>\n'
#       sys.exit(1)
#
#    day = sys.argv[1]
    day = os.environ["day"]
    add_day(day)


