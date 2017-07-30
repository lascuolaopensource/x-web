#!/usr/bin/python

# rimuove i .0 alla fine delle stringhe alla colonna data per il csv dato
# uso: numeri.py [colonna] [inputfile.csv] [outputfile.csv]
#                            (se outputfile.csv non viene dato come argomento salva sull'input)

# se proprio dovete rompere i coglioni:
# pisanti.nicola@gmail.com

import csv
import sys
import os

index = int( sys.argv[1] )
pathIn = sys.argv[2]

if len(sys.argv)<4 :
    pathOut = sys.argv[2]
else :
    pathOut = sys.argv[3]

print( "reading csv" )
reader = csv.reader(open(pathIn)) # Here your csv file
lines = [l for l in reader]
print( "...read" )

print( "changing strings" )
for line in lines :
    line[index] = line[index].split('.')[0]

print( "writing to csv" )
writer = csv.writer(open(pathOut, 'w'))
writer.writerows(lines)
print( "...done" )
