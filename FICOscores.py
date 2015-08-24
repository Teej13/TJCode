# 1. Import the relevant libraries
import pandas as pd
import matplotlib.pyplot as plt

#2 Read in data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#3 Drop null values
loansData.dropna(inplace=True)

#4 Print the first 5 rows of each of the column to see what needs to be cleaned
print loansData['Interest.Rate'][0:5]
print loansData['Loan.Length'][0:5]
print loansData['FICO.Range'][0:5]


#5 Clean up the columns in question (they are objects, have things appended to them) using lambda map
#First, interest rate
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
#Second, loan length
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
# Double Check that both worked
loansData['Interest.Rate'][0:5]
loansData['Loan.Length'][0:5]


#6 Parse the FICO scores, take the lowest (split) value
# Question - how can we run a test to be sure that each first value is the first?
# Another question - how 

loansData['FICO.Range'] = loansData['FICO.Range'].map(lambda x: x.split('-'))
loansData['FICO.Range'] = loansData['FICO.Range'].map(lambda x: [int(n) for n in x])
loansData['FICO.Score'] = loansData['FICO.Range']. map(lambda x: x[0])









# Plot histogram
plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

# Create a scatterplot matrix
a = pd.scatter_matrix(loansData, alpha=0.05, figure=(10, 10))
plt.show()

a = pd.scatter_matrix(loansData, alpha=0.05, figure=(10, 10), diagonal='hist')
plt.show()