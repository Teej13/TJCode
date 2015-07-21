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


#7. Plot the histogram
plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

#8 Generate the scatterplot matrix
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10))
plt.show()

a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()



# ***** ON TO REGRESSION ANALYSIS *****

#1. Import Additional Libraries
import numpy as np
import statsmodels.api as sm

#2 Set up the variables we need
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']


#3 Reshape the data
# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#Set up an input matrix, stacking up x1 and x2
x = np.column_stack([x1,x2])


#4 Put together the linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
# show the results summary
f.summary()

# Pulled down an interesting way to look at results
print 'Coefficients: ', f.params[1:]
print 'Intercept: ', f.params[0]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared

print "Final model: 'Interest Rate = " + str(round(f.params[0])) + " + " + str(f.params[1]) + "*fico" + ' + ' + str(f.params[2]) + "*loanamt"


# Output the data for later
loansData.to_csv('loansData_clean.csv',header=True,index=False)


