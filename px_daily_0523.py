import numpy as np
import pandas as pd
import datetime
from sklearn.model_selection import GridSearchCV
import datetime
from sklearn.metrics import mean_squared_error , mean_absolute_error, median_absolute_error

from regression import data_split2, feature_rearrange, fs_model_parm
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
from sklearn.svm import SVR


from sklearn.kernel_ridge import KernelRidge
################################################ Import & Transform data set
df = pd.read_csv('px_0523.csv', delimiter= ',')

Xall = df.iloc[:,8:]
yall = df.iloc[:,7]

################################################## Training: 2015.1 ~ 2016.6 #########################################

nstart1 = 0; ntest1 = 338;
X, Xtest = data_split2(Xall, nstart1, ntest1);
y, ytest = data_split2(yall, nstart1, ntest1)

X, Xtest, y, ytest, dfx = feature_rearrange(Xall, yall, nstart1, ntest1, mode='MRMR')

datey = df[['DATE.Y']]
datey = np.concatenate( np.array(datey[ntest1:]) )
monthy = df[['MONTH.Y']]
monthy = np.concatenate( np.array(monthy[ntest1:]) )
monthy = pd.to_datetime(pd.Series(monthy), format = '%Y%m' )
monthy = monthy.apply(lambda x: x.strftime('%Y-%m'))
weeky = df[['WEEK.Y']]
weeky = np.concatenate( np.array(weeky[ntest1:]) )

############################################################## GLM Regression

models = [#('linear', LinearRegression()),
          ('ridge', GridSearchCV( Ridge(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.001,10,100)})),
          ('lasso', GridSearchCV( Lasso(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.001,10,100)})),
          ('elastic-net', GridSearchCV(ElasticNet(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.01, 10, 100)})),
          ('kr', GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5, param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3], "gamma": np.logspace(-2, 2, 5)}))
          ]

res_feature_num, res_method, res_model, res_predicted, res_accuracy = fs_model_parm(X, Xtest, y, ytest , models,'rmse')

print('Feature Name: %s' % list( dfx.iloc[:,:res_feature_num].columns.values ) )

##### Plot & Check the accuracy
pddf1 = pd.DataFrame({'date':datey, 'ytest':ytest, 'res_predicted':res_predicted})
pddf1 = pddf1.set_index('date')
day1 = pddf1.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Daily data')
fig = day1.get_figure()
fig.savefig('GLM_daily.jpg')

rmse = np.sqrt(mean_squared_error(res_predicted, ytest))
print("GLM RMSE %f" % rmse )

###### Group by monthy
pddf11 = pd.DataFrame({'month':monthy, 'ytest':ytest, 'res_predicted':res_predicted})
pddf11 = pddf11.set_index('month')
pddf11 = pddf11.groupby(['month'])['res_predicted','ytest'].mean()
month1 = pddf11.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Monthly data')
fig = month1.get_figure()
fig.savefig('GLM_month.jpg')

###### Group by weeky
pddf12 = pd.DataFrame({'week':weeky, 'ytest':ytest, 'res_predicted':res_predicted})
pddf12['week'] = pddf12['week'].apply(str)
pddf12 = pddf12.set_index('week')
pddf12 = pddf12.groupby(['week'])['res_predicted','ytest'].mean()
week1 = pddf12.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Weekly data')
fig = week1.get_figure()
fig.savefig('GLM_week.jpg')


############################################################## SVR Regression
models = [('svr_linear', GridSearchCV(SVR(kernel='linear', gamma=0.1), cv=5,param_grid={"C": [1e0, 1e1, 1e2, 1e3],"gamma": np.logspace(-2, 2, 5)}))
          ]

res_feature_num1, res_method1, res_model1, res_predicted1, res_accuracy1 = fs_model_parm(X, Xtest, y, ytest , models,'rmse')

print('Feature Name: %s' % list( dfx.iloc[:,:res_feature_num1].columns.values ) )

##### Plot & Check the accuracy
pddf2 = pd.DataFrame({'date':datey, 'ytest':ytest, 'res_predicted':res_predicted1})
pddf2 = pddf2.set_index('date')
day2 = pddf2.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Daily data')
fig = day2.get_figure()
fig.savefig('GLM_daily.jpg')

rmse = np.sqrt(mean_squared_error(res_predicted, ytest))
print("GLM RMSE %f" % rmse )

###### Group by monthy

pddf21 = pd.DataFrame({'month':monthy, 'ytest':ytest, 'res_predicted':res_predicted1})
pddf21 = pddf21.set_index('month')
pddf21 = pddf21.groupby(['month'])['res_predicted','ytest'].mean()
month2 = pddf21.plot(figsize=(12,8),title = 'SVR - Training: 2015/01~2016/06 Monthly data')
fig = month2.get_figure()
fig.savefig('GLM_month.jpg')

###### Group by weeky

pddf22 = pd.DataFrame({'week':weeky, 'ytest':ytest, 'res_predicted':res_predicted1})
pddf22['week'] = pddf22['week'].apply(str)
pddf22 = pddf22.set_index('week')
pddf22 = pddf22.groupby(['week'])['res_predicted','ytest'].mean()
week2 = pddf22.plot(figsize=(12,8),title = 'SVR - Training: 2015/01~2016/06 Weekly data')
fig = week2.get_figure()
fig.savefig('GLM_week.jpg')





################################################## training: 2015.4 ~ 2016.9 #########################################
nstart1 = 54; ntest1 = 379;

X, Xtest = data_split2(Xall, nstart1, ntest1);
y, ytest = data_split2(yall, nstart1, ntest1)

datey = df[['DATE.Y']]
datey = np.concatenate( np.array(datey[ntest1:]) )
monthy = df[['MONTH.Y']]
monthy = np.concatenate( np.array(monthy[ntest1:]) )
monthy = pd.to_datetime(pd.Series(monthy), format = '%Y%m' )
monthy = monthy.apply(lambda x: x.strftime('%Y-%m'))
weeky = df[['WEEK.Y']]
weeky = np.concatenate( np.array(weeky[ntest1:]) )

X2, Xtest2, y2, ytest2, dfx2 = feature_rearrange(Xall, yall, nstart1, ntest1,  mode='MRMR')


############################################################## GLM Regression

models = [#('linear', LinearRegression()),
          ('ridge', GridSearchCV( Ridge(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.001,10,100)})),
          ('lasso', GridSearchCV( Lasso(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.001,10,100)})),
          ('elastic-net', GridSearchCV(ElasticNet(fit_intercept=True), cv=5, param_grid={"alpha": np.linspace(.01, 10, 100)})),
          ('kr', GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5, param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3], "gamma": np.logspace(-2, 2, 5)}))
          ]

res_feature_num2, res_method2, res_model2, res_predicted2, res_accuracy2 = fs_model_parm(X2, Xtest2, y2, ytest2 , models,'rmse')

print('Feature Name: %s' % list( dfx2.iloc[:,:res_feature_num2].columns.values ) )

##### Plot & Check the accuracy
pddf1 = pd.DataFrame({'date':datey, 'ytest':ytest, 'res_predicted':res_predicted2})
pddf1 = pddf1.set_index('date')
day1 = pddf1.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Daily data')
fig = day1.get_figure()
fig.savefig('GLM_daily.jpg')

rmse = np.sqrt(mean_squared_error(res_predicted2, ytest))
print("GLM RMSE %f" % rmse )

###### Group by monthy
pddf11 = pd.DataFrame({'month':monthy, 'ytest':ytest, 'res_predicted':res_predicted2})
pddf11 = pddf11.set_index('month')
pddf11 = pddf11.groupby(['month'])['res_predicted','ytest'].mean()
month1 = pddf11.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Monthly data')
fig = month1.get_figure()
fig.savefig('GLM_month.jpg')

###### Group by weeky
pddf12 = pd.DataFrame({'week':weeky, 'ytest':ytest, 'res_predicted':res_predicted2})
pddf12['week'] = pddf12['week'].apply(str)
pddf12 = pddf12.set_index('week')
pddf12 = pddf12.groupby(['week'])['res_predicted','ytest'].mean()
week1 = pddf12.plot(figsize=(12,8),title = 'GLM - Training: 2015/01~2016/06 Weekly data')
fig = week1.get_figure()
fig.savefig('GLM_week.jpg')





