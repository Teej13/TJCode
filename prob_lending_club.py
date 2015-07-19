# A: Boxplot, histogram, and QQ-plot for the values in the "Amount.Funded.By.Investors" 

#1. Set up libraries
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

#2 Read in data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#3 Drop null values
loansData.dropna(inplace=True)

#4 List the full data
#print loansData

#5 Set up a box plot on the amount requested column 
loansData.boxplot(column='Amount.Funded.By.Investors')
plt.show()
plt.savefig("boxplot_amountfunded.png")

#6 Set up a histogram on the amount requested column
loansData.hist(column='Amount.Funded.By.Investors')
plt.show()
plt.savefig("boxplot_amountfunded.png")

#7 Set up a QQ plot on the amount requested column
plt.figure()
graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)
plt.show()
plt.savefig("QQplot_amountfunded.png")



# B: Boxplot, histogram, and QQ-plot for the values in the "Amount.Requested" 

#1. Set up libraries
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

#2 Read in data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#3 Drop null values
loansData.dropna(inplace=True)

#4 List the full data
#print loansData

#5 Set up a box plot on the amount requested column 
loansData.boxplot(column='Amount.Requested')
plt.show()
plt.savefig("boxplot_amountrequested.png")

#6 Set up a histogram on the amount requested column
loansData.hist(column='Amount.Requested')
plt.show()
plt.savefig("boxplot_amountrequested.png")

#7 Set up a QQ plot on the amount requested column
plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.show()
plt.savefig("QQplot_amountrequested.png")
