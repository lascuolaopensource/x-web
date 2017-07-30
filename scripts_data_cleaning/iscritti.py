#!/usr/bin/python

# dai documenti dati genera un JSON con gli utenti di tutti i corsi
# ritrova anche le coordinate dei punti di origine dei differenti iscritti e calcola la distanza da Bari

# accede ai documenti settati in form_ids
# per funzionare bisogna generare il file di credentials secondo le istruzioni date dalla libreria gspread
# e bisogna dare l'accesso dei file online alla email che risulta dai credentials.json

# se proprio dovete rompere i coglioni:
# pisanti.nicola@gmail.com

import json
import gspread
import os.path
from oauth2client.client import SignedJwtAssertionCredentials
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import great_circle

geolocator = Nominatim()

if not os.path.isfile('credentials.json'):
    print "Credentials file missing, follow the instructions in the readme!"
    exit

json_key = json.load(open('credentials.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)

form_ids =[ [ "TYPE DESIGN", "11qjGcNKyFfctTFtfqBecPVq48hEGD_NeprQnT1LV35g"],
            [ "VISUAL STUDIES", "1WKRjvytGC29MI4BITsaj6oRy3hzLNx7vCb5q67eQRVU"],
            [ "MYO ROBOTIC BARTENDER", "12QNd2sjx9-vPPIWbX32TVYFdvx1GlaVzkXTtcQtpcuk" ],
            [ "DATA VISUALIZATION", "1tCMDh3cLUD3KO0h1UkFN785J46HW-ahEaEmFcqIeQT8" ],
            [ "BASIC DESIGN", "16gUUVgc--P1j8OvLJOm2miodPgjGDniySa_OrwK7HOk" ],
            [ "ELECTRONIC PROTOTYPING WORKSHOP", "1Nutyh708KkfAOb6zGQEveqp9nSZdkG8xXMYQKDI5v10" ],
            [ "SERIGRAPHY WORKSHOP", "14L12XORN2xXG3KeDHgZrMZYqbHqr2YK-WNtwWjC3Mvk" ],
            [ "PROCESS & SERVICE DESIGN WORKSHOP", "1OxVCz9OX1nbvTl8lOkZ-AwNi-PArlcVG1vnQ8fvGR_w" ],
            [ "POLITICAL COMMUNICATION WORKSHOP", "18V8qvUcLpOwQ96eeBlcnjcTZH7YbIk6Bq5WgVbtNEhM" ],
            [ "COMMUNICATION DESIGN", "1fYqx85j6Mo--zEjOYvxpXFj1M_ddMEwx6VJEwSEVgzI" ] ]

output = []

# l'indirizzo di SOS
while True :
    try:
        bari = geolocator.geocode( "Strada Lamberti 16, Bari" )
        break
    except GeocoderTimedOut as e:
        print("Error: geocode failed, retrying...")


for entry in form_ids :
    print( "operating on course "+ entry[0] + " with id " + entry[1] )
    doc = gc.open_by_key( entry[1] )

    worksheet = doc.get_worksheet(0)
    data = worksheet.get_all_values()

    fields_name = data[0]

    for row in data[1:] :
        output.append( dict(zip(fields_name, row)) ) 
        output[-1]["Nome / Name"]       = output[-1]["Nome / Name"].capitalize()
        output[-1]["Cognome / Surname"] = output[-1]["Cognome / Surname"].capitalize()
        output[-1]["Codice Fiscale / Fiscal Code"] = output[-1]["Codice Fiscale / Fiscal Code"].upper()        
        output[-1][u"Citt\u00e0 / City"] = output[-1][u"Citt\u00e0 / City"].capitalize()    

        address_string = output[-1][u"Indirizzo / Address"] + ", "+ output[-1][u"Citt\u00e0 / City"]
        #address_string = output[-1][u"Citt\u00e0 / City"]
        
        while True :
            try:
                location =  geolocator.geocode( address_string )
                if location is None : # if location is not found we try just the city without address
                    while True :
                        try:
                            location =  geolocator.geocode( output[-1][u"Citt\u00e0 / City"] )
                            break
                        except GeocoderTimedOut as e:
                            print("Error: geocode failed, retrying...")
                break
            except GeocoderTimedOut as e:
                print("Error: geocode failed, retrying...")

        if location is None :
            print( output[-1]["Nome / Name"] + " " + output[-1]["Cognome / Surname"] )
            print( output[-1][u"Citt\u00e0 / City"] + " location not found")
            output[-1]["Location"] = { "Longitude": "", "Latitude": "" }
            output[-1]["Distance"] = 0
        else :
            output[-1]["Location"] = {"Longitude": location.longitude, "Latitude": location.latitude}
            destination = (bari.longitude, bari.latitude)
            origin = (location.longitude, location.latitude)
            output[-1]["Distance"] = great_circle( origin, destination ).kilometers
        
print( "cleaning duplicates" )

newOutput = []
codici = []

for row in output :
    codice = row["Codice Fiscale / Fiscal Code"] 
        
    if codice not in codici :
        codici.append( codice )
        newOutput.append( row )
        output[-1]["Distance"]

output = newOutput 
    
with open( 'utenti_corsi.json', 'w') as outfile:
    json.dump( output, outfile, indent=4, sort_keys=True)

