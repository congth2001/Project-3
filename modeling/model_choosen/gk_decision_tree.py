import pickle
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import PowerTransformer, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

gk = pd.read_csv('./data/final_gk.csv')

X = gk.drop(['Tournament','Player','Nation','Age','Market_value','Min'],axis=1)
y = gk['Market_value']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Pre-processing

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

#Fitting data into first DecisionTree to get important features

#Initiating DecisionTreeRegressor
DtReg = DecisionTreeRegressor()

DtReg.fit(X_train_scaled,y_train)

#Extracting Most Important Features

feat_importances = pd.Series(DtReg.feature_importances_, index=X_train.columns)

#Creating a list of top features
top_features = list(feat_importances.nlargest(10).keys())
print(top_features)

#Repeating Workflow. This time only with most important features.

#This is because of computational constraints from GridSearching over 500 features.
X = gk.drop(['Tournament','Player','Nation','Age','Market_value','Min'],axis=1)[top_features]
y = gk['Market_value']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)

#Pre-processing

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

#GridSearching improved hyperparameters

# Hyper parameters range intialization for tuning 

parameters={"splitter":["best","random"],
            "max_depth" : [1,3,5,7,9,11,12],
           "min_samples_leaf":[1,2,3,4,5,6,7,8,9,10],
           "min_weight_fraction_leaf":[0.1,0.2,0.3,0.4,0.5],
           "max_features":["auto","log2","sqrt",None],
           "max_leaf_nodes":[None,10,20,30,40,50,60,70,80,90] }

tuning_model=GridSearchCV(DtReg,param_grid=parameters,scoring='neg_root_mean_squared_error',cv=5,verbose=3,error_score='raise')

tuning_model.fit(X_train_scaled,y_train)


#Extracting the best Parameters
param_values = list((tuning_model.best_params_).values())
        
# Traning model with all features using better Decision Tree Hyperparameters

#Initiating a new DecisionTreeRegressor
DtReg_Grid = DecisionTreeRegressor(max_depth=param_values[0],
                                 max_features=param_values[1],
                                 max_leaf_nodes=param_values[2],
                                 min_samples_leaf=param_values[3],
                                 min_weight_fraction_leaf=param_values[4],
                                 splitter=param_values[5])

DtReg_Grid.fit(X_train_scaled,y_train)
print
pickle.dump(DtReg_Grid, open('./model_gk.pkl','wb'))
print(top_features)