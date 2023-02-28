import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PowerTransformer, RobustScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

df=pd.read_csv('./data/final.csv')
midfield = df[df['Position']=='Midfielder']

#Initiating a results Dataframe
lr_results = pd.DataFrame(columns=['Train/Test','Avg RMSE','Max RMSE','Min RMSE'])

#Finding top 10 correlated features
top_features = list((abs(midfield.corr()['Market_value'])).sort_values(ascending=False)[1:11].keys())
print(top_features)

#Separating target variable - 'Value'. Only top 10 features are included in X.
X = midfield[top_features]
y = midfield['Market_value']

#Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

############################################################################

#Making the distribution of the features more Gaussian

pt = PowerTransformer()

X_train_transformed = pt.fit_transform(X_train)
X_test_transformed = pt.transform(X_test)


#Scaling the data

#Initiating Robust Scaler
rs= RobustScaler()

#Standardizing numerical columns
X_train_scaled = rs.fit_transform(X_train_transformed)
X_test_scaled = rs.transform(X_test_transformed)


#Initiating the Linear Regressor
lr = LinearRegression()

#Fitting the Linear Regressor with Training Data
lr.fit(X_train_scaled,y_train)

# lr.intercept_

# vals=[1, 40, 10, 20, 21, 10, 66, 10, 66, 49]
# lr.predict([vals])

pickle.dump(lr, open('./model_mf.pkl','wb')) 