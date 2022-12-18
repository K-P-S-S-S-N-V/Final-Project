# -*- coding: utf-8 -*-
"""predicting breast cancer in patient.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P_lItRZMPPahWU19gCUJC4o89LN24gnk
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv(r"cancer.csv")
print(df)

df.isnull().sum()

df.drop(columns=["Unnamed: 32"], inplace=True)

del df['id']
print(df)

df.describe()

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()

df = df.drop_duplicates()
x = df.loc[:,df.columns[1:]]
y = df['diagnosis']
y = y.map({'M':1, 'B':0})

!pip install sklearn

# Commented out IPython magic to ensure Python compatibility.
# %pip install scikit-learn

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.30, random_state=4)
print("x_train-shape : ", x_train.shape)
print("y_train-shape : ", y_train.shape)
print("x_test-shape : ", x_test.shape)
print("y_test-shape : ", y_test.shape)

def capping(df,cols):
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        Up=Q3 + (1.5 * IQR)
        Low=Q1 - (1.5 * IQR)
        
        df[col]=np.where(df[col]> Up,Up,np.where(df[col]<Low,Low,df[col]))

cols=x_train.columns
print(cols)

capping(x_train,cols)
x_train.describe()

Q1 = x_train.quantile(0.25)
Q3 = x_train.quantile(0.75)
IQR = Q3 - Q1
((x_train < (Q1 - 1.5 * IQR)) | (x_train > (Q3 + 1.5 * IQR))).sum()

from sklearn.preprocessing import StandardScaler

std = StandardScaler()

x_train = std.fit_transform(x_train)
x_test = std.transform(x_test)

from sklearn.svm import SVC

SVM = SVC(kernel='linear', gamma='scale')
SVM.fit(x_train, y_train)

y_pred = SVM.predict(x_test)
print(y_pred)

df_new = pd.DataFrame({'True_Target': y_test, 'Predicted_target': y_pred})
print(df_new)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cnf_matrix_test = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cnf_matrix_test, display_labels=SVM.classes_).plot()

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("The model accuracy is", accuracy )

group_names = ["True Pos","False Pos","False Neg","True Neg"]
group_counts = ["{0:0.0f}".format(value) for value in cm.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in cm.flatten()/np.sum(cm)]
labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
labels = np.asarray(labels).reshape(2,2)

sns.heatmap(cm, annot=labels, fmt="", cmap='Blues')

from sklearn.metrics import classification_report
predictions = SVM.predict(x_test)
print(classification_report(y_test, predictions))

from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.1, 1, 10, 100, 1000], 
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf']} 

grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 

grid.fit(x_train, y_train)

print(grid.best_params_)
print(grid.best_estimator_)

grid_predictions = grid.predict(x_test)
print(classification_report(y_test, grid_predictions))

cm = confusion_matrix(y_test, grid_predictions)

group_names = ["True Pos","False Pos","False Neg","True Neg"]
group_counts = ["{0:0.0f}".format(value) for value in cm.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in cm.flatten()/np.sum(cm)]
labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
labels = np.asarray(labels).reshape(2,2)

sns.heatmap(cm, annot=labels, fmt="", cmap='Blues')

