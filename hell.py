import sys
import pandas as pf
import csv
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print str(sys.argv[1]);
r = pf.read_csv('/home/salman/Desktop/only_isbn.csv')
r.head()
print(r.head())
