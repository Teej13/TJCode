#Probability Distributions and Frequencies

# 1. Set up libraries needed
import matplotlib.pyplot as plt
import numpy as np 
import scipy.stats as stats
import collections

#2 Import the data as x
test_data = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

#3 Derive frequencies
c = collections.Counter(test_data)
print c
count_sum = sum(c.values())
for k,v in c.iteritems():
  print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

#4. Run and save box plot
plt.boxplot(test_data)
plt.show()
plt.savefig("boxplot.png")

#5 Run and save histogram
plt.hist(test_data, histtype='bar')
plt.show()
plt.savefig("histogram.png")

#6 Set up Q-Q plots
plt.figure()
#test_data = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
graph1 = stats.probplot(test_data, dist="norm", plot=plt)
plt.show()

