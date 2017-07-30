#!/usr/bin/python

# divide i nomi alla colonna data da nome+cognome a due colonne separate per nome e cognome
# la colonna viene aggiunta dopo la colonna data
# uso: dividi_nomi.py [colonna] [inputfile.csv] [outputfile.csv]
#                            (se outputfile.csv non viene dato come argomento salva sull'input)

# se proprio dovete rompere i coglioni:
# pisanti.nicola@gmail.com

import csv
import sys
import os

# parsing input
index = int( sys.argv[1] )
pathIn = sys.argv[2]

if len(sys.argv)<4 :
    pathOut = sys.argv[2]
else :
    pathOut = sys.argv[3]

print( "reading csv" )
reader = csv.reader(open(pathIn)) # Here your csv file
table = [l for l in reader]
print( "...read" )

print( "changing strings" )

for row in table:
    splitted = row[index].split(' ')

    # first letter uppercase, the other lowercase
    for word in splitted :
        word = word.capitalize()

    if len(splitted) <= 1 :
        
        row.insert((index + 1), '')
   
    elif len(splitted) == 2 :
   
        row[index] = splitted[0]
        row.insert((index + 1), splitted[1])    
   
    else :
        
        joinRange = -1
        if splitted[-2] in [ "Di", "Del", "Della", "Dello", "Dei", "La", "Lo", "Li", "Le" ] : 
            joinRange = -2
        
        # join strings and set name
        joined = ""
        for word in splitted[:joinRange] :
            joined = joined + word
            joined = joined + " "
        joined = joined[:-1] # remove last whitespace
        
        row[index] = joined
        
        # join strings and set surname
        joined = ""
        for word in splitted[joinRange:] :
            joined = joined + word
            joined = joined + " "
        joined = joined[:-1] # remove last whitespace
        
        row.insert((index + 1), joined)  
    

print( "writing to csv" )
writer = csv.writer(open(pathOut, 'w'))
writer.writerows(table)
print( "...done" )

