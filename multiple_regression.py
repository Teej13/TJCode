# Multiple Regression Analysis

#1 Import relevant libraries - key one here is statsmodels 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf 

#2 Read in data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#3 Drop null values
loansData.dropna(inplace=True)

#4 Clean up the columns in question (they are objects, have things appended to them) using lambda map
#First, interest rate
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
#Second, loan length
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
# Double Check that both worked
loansData['Interest.Rate'][0:5]
loansData['Loan.Length'][0:5]


#5 Parse the FICO scores, take the lowest (split) value
# Question - how can we run a test to be sure that each first value is the first?
# Another question - how 

loansData['FICO.Range'] = loansData['FICO.Range'].map(lambda x: x.split('-'))
loansData['FICO.Range'] = loansData['FICO.Range'].map(lambda x: [int(n) for n in x])
loansData['FICO.Score'] = loansData['FICO.Range']. map(lambda x: x[0])

#6 Generate Dichotomous Variable for Above 12% Interest Rate
loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x > .12 else 0)

#7 Generate a constant intercept of 1
loansData['Intercept'] = 1

#8 Set up independent variables 
ind_vars = ['Intercept', 'FICO.Score','Amount.Requested']



# Now on to the multiple regression 
#9. Set up Variables. 

# IV1: Annual Income: Calculate from Monthly Income
annual_income = loansData['Monthly.Income']*12
annual_income[np.isnan(annual_income)] = 0
loansData['annual_income'] = annual_income

# IV 2: Home Ownership, Need to Account for Categorical Variable
# Categories (4, object): [MORTGAGE < OTHER < OWN < RENT]
# So, if value = 2, own. 
home_owner = pd.Categorical.from_array(loansData['Home.Ownership'])
loansData['Home.Ownership'] = home_owner.labels

# Control from Original 1: FICO Score
fico = loansData['FICO.Score']
fico[np.isnan(fico)] = 0

# Control from Original 2: Loan Amount 
loan_amount = loansData['Amount.Requested']
loan_amount[np.isnan(loan_amount)] = 0

# Model 1: 
# Set up vars for model
X = loansData[['annual_income', 'Home.Ownership']]
y = loansData['Interest.Rate']
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()
est.summary()

print('Coefficients: ', f.params[0:2])
print('Intercept: ', f.params[2])
print('P-Values: ', f.pvalues)
print('R-Squared: ', f.rsquared)


# Model 2: 
# Set up vars for model
X = loansData[['annual_income', 'Home.Ownership','FICO.Score','Amount.Requested']]
y = loansData['Interest.Rate']
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()
est.summary()

print('Coefficients: ', f.params[0:2])
print('Intercept: ', f.params[2])
print('P-Values: ', f.pvalues)
print('R-Squared: ', f.rsquared)

loansData.to_csv('LoanStats3b.csv',header=True,index=False)

