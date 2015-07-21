# Logistic Regression Analysis

#1 Import relevant libraries - key one here is statsmodels 
import pandas as pd 
import statsmodels.api as sm 
import collections
import matplotlib.pyplot as plt
import math

#2 Read in data - this time, local file that was cleaned in last lesson
loansData = pd.read_csv('loansData_clean.csv')

#3 Generate Dichotomous Variable for Above 12% Interest Rate
loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x > .12 else 0)

#4 Generate a constant intercept of 1
loansData['Intercept'] = 1

#5 Set up independent variables 
ind_vars = ['Intercept', 'FICO.Score','Amount.Requested']

#6 Set up a logit model, print results
X = loansData[ind_vars]
y = loansData['IR_TF']
logit = sm.Logit(y,X)

result = logit.fit()
coeff = result.params
print coeff # This will need to be plugged back in to the equation


#7 Set up a function to drop this info ind_vars
threshold = 0.7

print "The Logistic function will look like this: p(x) = 1/(1 + e^(intercept + 0.087423(FicoScore) − 0.000174(LoanAmount))"
# Set up the function
def logistic_function(FicoScore, LoanGrantAmount, coeff):
	prob = (1/(1+math.exp(coeff[0]+coeff[1]*FicoScore+coeff[2]*LoanGrantAmount)))
	if prob > threshold:
		p = 1
	else:
		p = 0
	return prob, p

prob = logistic_function(720, 10000, coeff)[0]
prediction = logistic_function(720, 1000, coeff)[1]

prob_approve = float(prob*100)
threshold_text = float(threshold*100)

print "The probability of getting a sub-12% interest rate $10,000 loan with a 720 FICO score is " + ("{0:.2f}".format(round(prob_approve,2))) + "%."
print "We can make a positive prediction if the probability threshold is " + str(threshold_text) + "%. " 

if prediction == 1:
	print "Thus, because the probability of getting a sub-12% interest rate $10,000 loan with a 720 FICO score is greater than " + str(threshold_text) + "%, we can safely predict that the loan will be approved." 
else: 
	print "Thus, because the probability of getting a sub-12% interest rate $10,000 loan with a 720 FICO score is less than " + str(threshold_text) + "%, we cannot safely predict that the loan will be approved." 


