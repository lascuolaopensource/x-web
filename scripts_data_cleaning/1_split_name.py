# Modules
import csv
import os



# Functions
def splitName(pathIn, pathOut, index):

    with open(pathIn, pathOut, 'rb') as csvFile:
        
        table = csv.reader(csvFile)

        for row in table:

            nameSurname = row[index]

            spaceCount = nameSurname.count(' ')

            if spaceCount == 0:
                row.insert((index + 1), '')

            elif spaceCount == 1:

                nameAndSurname = nameSurname.split(' ')

                row[index] = nameAndSurname[0]

                row.insert((index + 1), nameAndSurname[1])

            else:

                namesAndSurnames = nameSurname.split(' ')

                length = len(namesAndSurnames)

                penultimate = namesAndSurnames[length-1]

                if len(penultimate) <= 3:

                    actual = nameSurname.rsplit(' ', 1)

                    name = actual[0]
                    surname = actual[1]

                    row[index] = name
                    row.insert((index + 1), surname)

                else:

                    namesAndSurnames = nameSurname.rsplit(' ', 1)

                    row[index] = nameAndSurname[0]

                    row.insert((index + 1), nameAndSurname[1])

    csvFile = pathOut

    with open(csvFile, "w") as output:

        writer = csv.writer(output, lineterminator='\n')

        writer.writerows(table)





pIn = "/Users/giovanniabbatepaolo/Desktop/SOS/1 pulizia dati/someCsv"

pOt = "/Users/giovanniabbatepaolo/Desktop/SOS/1 pulizia dati/splitCsv"

file = "csvSplit--- Copia di domande d'iscrizione – XYZ (Bari, 18 - 30 luglio)__X - selezioni__1.csv"

splitName(pathIn = pIn+file, pathOut = pOt+file, index = 2)
