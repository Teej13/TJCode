# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas
import sqlite3 as lite
import matplotlib.pyplot as plt
import csv
import numpy

# Store the relevant URL
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

# Go get the HTML data
r = requests.get(url)

# Use Beautiful Soup to Parse the HTML
soup_data = BeautifulSoup(r.content)
#print soup('table')[6].prettify()


# Drill down to the table we care about 
soup_tag = soup_data('table')[6].tr.td
soup_table = soup_tag('table')[1].tr.td.div
raw_table = soup_table('table')[0]



col_name = []
for child in raw_table('tr'): 
    if child.get('class', ['Null'])[0] == 'lheader': 
        for td in child.find_all('td'): 
            if td.get_text() != '': 
                col_name.append(td.get_text())
        break
country_table = pandas.DataFrame(columns = col_name)

edu_row_num = 0
for child in raw_table('tr'):
    row_curr = []
    if child.get('class', ['Null']) == 'tcont':
        row_curr.append(child.find('td').get_text())
        for td in child.find_all('td')[1:]: 
            if td.get('align'): 
                row_curr.append(td.get_text())
    else: 
        row_curr.append(child.find('td').get_text())
        for td in child.find_all('td')[1:]:
            if td.get('align'): 
                row_curr.append(td.get_text())
    if len(row_curr) == len(col_name): 
        country_table.loc[edu_row_num] = row_curr
        edu_row_num += 1
        
country_table[['Total','Men', 'Women']] = country_table[['Total','Men', 'Women']].convert_objects(convert_numeric = True)

country_gdp = pandas.DataFrame(columns = ['country_name', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010'])

with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    gdp_row_num = 0
    for line in inputReader:
        row_curr = [line[0]]
        row_curr.extend(line[43:-5])
        country_gdp.loc[gdp_row_num] = row_curr
        gdp_row_num += 1
country_gdp[country_gdp.columns[1:-1]] = country_gdp[country_gdp.columns[1:-1]].convert_objects(convert_numeric = True)

country_table['GDP'] = numpy.nan
for i in range(edu_row_num): 
    find_index = country_gdp[country_gdp['country_name'] == country_table['Country or area'][i]].index
    if len(find_index) > 0: 
        row_index = find_index.tolist()[0]
        country_table['GDP'][i] = country_gdp[country_table['Year'][i]][row_index]
edu_gdp = country_table[numpy.isfinite(country_table['GDP'])][['Country or area', 'Total', 'GDP']]
edu_gdp['log_GDP'] = numpy.log(edu_gdp['GDP'])
edu_gdp.plot(kind = 'scatter', x = 'Total', y = 'log_GDP')
plt.show()
