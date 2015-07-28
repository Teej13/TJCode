
#1. Import the relevant libraries 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

#2 read in the data
df = pd.read_csv('LoanStats3b.csv', header=1, low_memory=False)

#3 Convert string of the "issue_d" variable to datetime object in pandas:
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 

#4 Get a time series set together 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

#5 Show the summary on a time plot 
plt.plot(loan_count_summary)
plt.ylabel("Number of Loans")
plt.xlabel("Month")
plt.show()

#6 To get to a stationary time series, get the first differences 
loan_count_sum_diff = loan_count_summary.diff()
plt.plot(loan_count_sum_diff)
plt.show()

#7 Run the Autocorrelation
sm.graphics.tsa.plot_acf(loan_count_summary) #first moment 

#8 Run the Partial Autocorrelation
sm.graphics.tsa.plot_pacf(loan_count_summary) #first moment 




