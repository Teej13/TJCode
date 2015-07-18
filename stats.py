# 1. import the data
import pandas as pd

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

# 2. Split along thew newlines
data = data.splitlines()

# 3. Split on the commas
data = [i.split(', ') for i in data]

#4 Get to a pandas dataframe
column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

#5. set up the stats module
from scipy import stats

#6. Convert data types of Alcohol and Tobacco to Float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

#7. Print the means for Alcohol and Tobacco
print "The mean of alcohol consumption is %f" % df['Alcohol'].mean()
print "The mean of tobacco consumption is %f" % df['Tobacco'].mean()

#8 Print the medians for Alcohol and Tobacco
print "The median of alcohol consumption is %f" % df['Alcohol'].median()
print "The median of tobacco consumption is %f" % df['Tobacco'].median()

#9 Print the modes for Alcohol and Tobacco
AlcoholMode=stats.mode(df['Alcohol'])
TobaccoMode=stats.mode(df['Tobacco'])
print "The mode of the alcohol and tobacco is %.2f %.2f, respectively" %(AlcoholMode[0], TobaccoMode[0])

#10 Print the range for Alcohol and Tobacco
print "The range of Alcohol consumption is ", max(df['Alcohol']) - min(df['Alcohol'])
print "The range of Tobacco consumption is ", max(df['Tobacco']) - min(df['Tobacco'])

#11 Print the variance for Alcohol and Tobacco
print "the variance of Alcohol consumption is %f" % df['Alcohol'].var() 
print "the variance of Tobacco consumption is %f" % df['Tobacco'].var() 

#12 Print the Standard Deviation for Alcohol and Tobacco
print "The standard variation of Alcohol consumption is %s" % df['Alcohol'].std() 
print "The standard variation of Tobacco consumption is %s" % df['Tobacco'].std() 