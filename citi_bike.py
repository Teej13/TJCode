#1. Import relevant libraries
import requests
import pandas as pd 
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
import collections 
import sqlite3 as lite
from dateutil.parser import parse
import time

#2. Go get the data
r = requests.get('http://www.citibikenyc.com/stations/json')

#3 Take a look at the data, in JSON format
r.json().keys() #look at the keys

#4 Develop the key list 
key_list = []
for station in r.json()['stationBeanList']:
	for k in station.keys():
		if k not in key_list:
			key_list.append(key_list)

r.json()['stationBeanList'][0] #look at the first element

#5 Get the JSON Data into a Pandas dataframe 
df = json_normalize(r.json()['stationBeanList'])

#6 Look at the range of values, visually
df['availableBikes'].hist() #available bikes
plt.show()

df['totalDocks'].hist() #total docks
plt.show()

# Do we need to do the same exercise for the Execution Time side of things?

#7. Challenges
#a. Are there any test stations?
len(r.json()['stationBeanList']) # Total records
collections.Counter(df['testStation']) # Number of non-test records
# no difference, so no test stations

#b What's the mean/median number of bikes in a dock?
print 'The mean number of available bikes is ' + str(df['availableBikes'].mean())
print 'The median number of available bikes is ' + str(df['availableBikes'].median())
# how does that change conditional on the dock being in service? 
condition = (df['statusValue'] == 'In Service')
print 'The mean number of available bikes from in-service docks is ' + str(df[condition]['availableBikes'].mean())
print 'The median number of available bikes from in-service docks is ' + str(df[condition]['availableBikes'].median())



###### TIME TO STORE THE DATA ####

#1. Set up SQL Database 
con = lite.connect('citi_bike.db')
cur = con.cursor()

#2. Create a table to store the data
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#3. Set up statement to run again and again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#4. Set up the for loop to populate the database
with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#5. Port over the station ID 
station_ids = df['id'].tolist() 
tation_ids = ['_' + str(x) + ' INT' for x in station_ids]  #clean up for SQL

#6. Bring it together
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");") 
    
#7. Convert the string to a daytime object    
exec_time = parse(r.json()['executionTime'])    

with con:
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

#8. Iterate through the stations in the "stationBeanList":
id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

#loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

#iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
    
### NOW, SET UP TO DO THIS EVERY MINUTE FOR AN HOUR ####

con = lite.connect('citi_bike.db')
cur = con.cursor()

for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
    con.commit()

    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
    con.commit()

    time.sleep(60)

con.close() #close the database connection when done



## NEXT, EXTRACT JUST THE DATA OF INTEREST ##

con = lite.connect('citi_bike.db')
cur = con.cursor()
df = pd.read_sql("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer
  
def keywithmaxval(d):
    # create a list of the dict's keys and values; 
    v = list(d.values())
    k = list(d.keys())

    # return the key with the max value
    return k[v.index(max(v))]

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

plt.bar(hour_change.keys(), hour_change.values())
plt.show()
   