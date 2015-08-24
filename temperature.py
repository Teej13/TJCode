# import relevant libraries 
import requests
import sqlite3 as lite
import datetime
import json
import pandas as pd
import numpy as np

# Set API key and URL
API_key = "9c6663f4e31651590a6c9b1fa95491a9"
URL = 'https://api.forecast.io/forecast/' + API_key


# Develop the list of cities
cities = {"Atlanta": '33.762909,-84.422675',
			"Austin": '30.303936,-97.754355',
			"Boston": '42.33196,-71.020173',
			"Chicago": '41.837551,-87.681844',
			"Cleveland": '41.478462,-81.679435',
			"Denver": '39.76185,-104.881105',
			"Las Vegas": '36.229214,-115.26008',
			"Los Angeles": '34.019394,-118.410825',
			"Miami": '25.775163,-80.208615'
        }


city_keys = cities.keys()
city_columns = [ str(x) + ' INT' for x in city_keys]

       
end_date = datetime.datetime.now() # by setting this equal to a variable, we fix the calculation to the point when we started the scrip (rather than have things move aroudn while we're coding.)
        
        
# Connect to the a defined database
con = lite.connect('weather.db')
cur = con.cursor()        

#Create the table

with con:
    cur.execute ("DROP TABLE IF EXISTS daily_temp")
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, "Atlanta" REAL, "Boston" REAL, "Chicago" REAL, "Denver" REAL, "Las Vegas" REAL, "Los Angeles" REAL, "Miami" REAL);')

query_date = end_date - datetime.timedelta(days =30)


# Populate the table with values
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%Y%m%d')),))
        query_date += datetime.timedelta(days=1)

#Now loop through our cities and query the API:

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(URL + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
			
        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day

con.close() # a good practice to close connection to database        




#Query the database and get stats to answer questions
con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading", con ,index_col='day_of_reading')

print "\n"
for k,v in cities.iteritems():
    print str(k) + " mean is: " + str(df[k].mean())
    print str(k) + " median is: " + str(df[k].median())
    print str(k) + " variance is: " + str(np.var(df[k]))
    print str(k) + " fluctuation based on difference between max and min is: " + str(np.amax(df[k])-np.amin(df[k]))
    print "\n"


con.close()

