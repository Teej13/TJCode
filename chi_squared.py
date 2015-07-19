# Do Chi-Sq test on the data

#1. Import libraries
from scipy import stats
import collections
import pandas as pd
import matplotlib.pyplot as plt

#2. Read in data, clean it up
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

#3. Develop a frequency variable
freq = collections.Counter(loansData['Open.CREDIT.Lines'])

print "The number of elements of the dataset is " +str(k)

# calculate the number of instances in the list
count_sum = sum(freq.values())

for k,v in freq.iteritems():
  print "The frequency of each number of credit lines" + str(k) + " is " + str(float(v) / count_sum)
  
#4 Plot it out   
plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

#5 Do a chi-sq test
chi, p = stats.chisquare(freq.values())
print (p, chi)