#Multiple Regression

#1. Import Libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm

#2. Read in the data
df_adv = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
X = df_adv[['TV', 'Radio']]
y = df_adv['Sales']
df_adv.head()

#3. Set up the regression model
X = df_adv[['TV', 'Radio']]
y = df_adv['Sales']

## fit a OLS model with intercept on TV and Radio
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()

est.summary()


#4. Even simpler:
# import formula api as alias smf
import statsmodels.formula.api as smf

# formula: response ~ predictor + predictor
est = smf.ols(formula='Sales ~ TV + Radio', data=df_adv).fit()


#5 Handling categorial variables
import pandas as pd

df = pd.read_csv('http://statweb.stanford.edu/~tibs/ElemStatLearn/datasets/SAheart.data', index_col=0)

# copy data and separate predictors and response
X = df.copy()
y = X.pop('chd')

df.head()

# compute percentage of chronic heart disease for famhist
y.groupby(X.famhist).mean()

# Set up the categorical var
import statsmodels.formula.api as smf

# encode df.famhist as a numeric via pd.Factor
df['famhist_ord'] = pd.Categorical(df.famhist).labels

est = smf.ols(formula="chd ~ famhist_ord", data=df).fit()


#6. Interaction Terms
df = pd.read_csv('https://raw2.github.com/statsmodels/statsmodels/master/'
                 'statsmodels/datasets/randhie/src/randhie.csv')
df["logincome"] = np.log1p(df.income)

df[['mdvis', 'logincome', 'hlthp']].tail()

# Because hlthp is a binary variable we can visualize the linear regression model by plotting two lines: one for hlthp == 0 and one for hlthp == 1.
plt.scatter(df.logincome, df.mdvis, alpha=0.3)
plt.xlabel('Log income')
plt.ylabel('Number of visits')

income_linspace = np.linspace(df.logincome.min(), df.logincome.max(), 100)

est = smf.ols(formula='mdvis ~ logincome + hlthp', data=df).fit()

plt.plot(income_linspace, est.params[0] + est.params[1] * income_linspace + est.params[2] * 0, 'r')
plt.plot(income_linspace, est.params[0] + est.params[1] * income_linspace + est.params[2] * 1, 'g')
short_summary(est)


# We can then include an interaction term to explore the effect of an interaction between the two -- i.e. we let the slope be different for the two categories.

plt.scatter(df.logincome, df.mdvis, alpha=0.3)
plt.xlabel('Log income')
plt.ylabel('Number of visits')

est = smf.ols(formula='mdvis ~ hlthp * logincome', data=df).fit()

plt.plot(income_linspace, est.params[0] + est.params[1] * 0 + est.params[2] * income_linspace + 
         est.params[3] * 0 * income_linspace, 'r')
plt.plot(income_linspace, est.params[0] + est.params[1] * 1 + est.params[2] * income_linspace + 
         est.params[3] * 1 * income_linspace, 'g')

short_summary(est)


loansData.to_csv('loansData_clean.csv',header=True,index=False)


