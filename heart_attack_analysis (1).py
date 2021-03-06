# -*- coding: utf-8 -*-
"""Heart Attack Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19t76UV_hcwED7ZfJt_AJPUU96Dbo_jjG
"""

# Commented out IPython magic to ensure Python compatibility.
 # Importing Libraries

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, roc_curve,plot_confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

import warnings
warnings.filterwarnings("ignore")

from google.colab import drive
drive.mount('/content/drive/')

# Loading Data

full_data = pd.read_csv("/content/drive/MyDrive/Heart Attack Analysis/heart (1).csv")
full_data

# Understanding data
print(full_data.head(3))
print("\nNumber of rows:",full_data.shape[0])
print("Number of columns:",full_data.shape[1])
print("Column names: ",list(full_data.columns))

# Data Description
full_data.describe().T.style.bar(subset=['mean'],color='Green').background_gradient(subset=['std'],cmap='Reds')

# checking NaN values

full_data.isna().sum()

# Function for checking outlier
def outlier_check(var):
  L_outlier = []
  R_outlier = []
  data = sorted(full_data[var])
  q1,q3 =  np.percentile(data,[25,75])
  iqr_val = q3-q1
  lower_bond = q1-(1.5*iqr_val)
  upper_bond = q3+(1.5*iqr_val)
  for i in data:
    if i<lower_bond:
      L_outlier.append(i)
    elif i>upper_bond:
      R_outlier.append(i)
  print("1st Quartile : ",q1,"\n3rd Quartile : ",q3)
  print("Inter quartile range : ",iqr_val)
  print("minimum value : ",min(data))
  print("maximum value : ",max(data))
  
  print("Lower bond value: ",lower_bond,"\nUpper bond value : ",upper_bond)
  print("Left Outlier: ",L_outlier)
  print("Right Outlier: ",R_outlier)
  #plt.boxplot(data, notch = True, vert = False)
  plt.boxplot(data,patch_artist = True,vert = False,
           boxprops = dict(facecolor = 'red', color = 'red'),
           whiskerprops = dict(color = 'green'),
           capprops = dict(color = 'blue'),
           medianprops = dict(color = 'yellow'))
  print("-------Outlier detection for column ",var,"-------")
  plt.show()

outlier_check('age')

outlier_check('trtbps')

outlier_check('chol')

outlier_check('thalachh')

outlier_check('oldpeak')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

# Univariate Analysis of Categorical Variables
fig, axes = plt.subplots(4,2, figsize=(18,18))

#use the axis for plotting
axes[0, 0].set_title('(Plot.1.1) SEX')
sns.countplot(full_data.sex,
              palette = 'Set3',
              edgecolor=sns.color_palette("Set3", 4),
              linewidth=2,
             ax=axes[0,0]);


#use the axis for plotting
axes[0, 1].set_title('(Plot.1.2)CP')
sns.countplot(full_data.cp,
              palette = 'Set1',
              edgecolor=sns.color_palette("Set1", 2),
              linewidth=2,
             ax=axes[0,1]);


#use the axis for plotting
axes[1, 0].set_title('(Plot.1.3)FBS')
sns.countplot(full_data.fbs,
              palette = 'Set2',
              edgecolor=sns.color_palette("Set2", 2),
              linewidth=2,
             ax=axes[1,0]);


#use the axis for plotting
axes[1, 1].set_title('(Plot.1.4)REST-ECG')
sns.countplot(full_data.restecg,
              palette = 'Blues_r',
              edgecolor=sns.color_palette('Blues_r', 4),
              linewidth=2,
             ax=axes[1,1]);


#use the axis for plotting
axes[2, 0].set_title('(Plot.1.5)EXNG')
sns.countplot(full_data.exng,
              palette = 'Oranges_r',
              edgecolor=sns.color_palette('Oranges_r', 4),
              linewidth=2,
             ax=axes[2,0]);


#use the axis for plotting
axes[2, 1].set_title('(Plot.1.6)SLOPE')
sns.countplot(full_data.slp,
              palette = 'autumn_r',
              edgecolor=sns.color_palette('autumn_r', 2),
              linewidth=2,
             ax=axes[2,1]);


#use the axis for plotting
axes[3, 0].set_title('(Plot.1.7)CAA')
sns.countplot(full_data.caa,
              palette = 'icefire_r',
              edgecolor=sns.color_palette('icefire_r', 2),
              linewidth=2,
             ax=axes[3,0]);


axes[3, 1].set_title('(Plot.1.8)THALL')
sns.countplot(full_data.thall,
              palette = 'summer',
              edgecolor=sns.color_palette('summer', 4),
              linewidth=2,
             ax=axes[3,1]);

plt.tight_layout(pad=3);

# Univariate Analysis of Continuous and Target Variables
fig, axes = plt.subplots(2,3, figsize=(15,12))

#use the axis for plotting
axes[0, 0].set_title('(Plot.2.1)AGE')
sns.boxenplot(y=full_data.age,
            palette='Greens', 
            color='red',
           linewidth=3,
           ax=axes[0,0]);


#use the axis for plotting
axes[0,1].set_title('(Plot.2.2)TRTBPS')
sns.boxenplot(y=full_data.trtbps,
            palette='prism', 
            color='red',
           linewidth=2,
           ax=axes[0,1]);


#use the axis for plotting
axes[0, 2].set_title('(Plot.2.3)CHOL')
sns.boxenplot(y=full_data.chol,
            palette='viridis',
           linewidth=1,
           ax=axes[0,2]);


#use the axis for plotting
axes[1, 0].set_title('(Plot.2.4)THALACHH')
sns.boxenplot(y=full_data.thalachh,
            palette='Blues_r', 
            color='red',
           linewidth=3,
           ax=axes[1,0]);


#use the axis for plotting
axes[1, 1].set_title('(Plot.2.5)OLDPEAK')
sns.boxenplot(y=full_data.oldpeak,
            palette='RdPu', 
            color='red',
           linewidth=3,
           ax=axes[1,1]);

print("-----Distribution of target variable-----")
#sns.countplot(full_data['output'])

value_count = full_data['output'].value_counts()
print(value_count)
h_attack = ["More Chance of Heart Attack","Less Chance of Heart Attack"]
plt.pie(value_count,labels = h_attack,autopct='%0.1f%%')
plt.show()

plt.figure(figsize = (12,10))
plt.title('(Plot.4.1) Correlation between variables')
sns.heatmap(full_data.corr(), fmt='.1f', annot=True, cmap= "bone_r");

# 01 Logistic Regression
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train,y_train) # model will learn form X_train and y_train

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix :\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy :",ac)

# 02 Decision Tree
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix:\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy :",ac)

# 03 Random Forest
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.ensemble import RandomForestClassifier # It is created with many decision tree
classifier = RandomForestClassifier(n_estimators=10) # How many tree we want to take
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix:\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy:",ac)

# 04 Support Vector Classifier
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.svm import SVC # Support Vector Classifier
classifier = SVC()
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix:\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy :",ac)

# 05 KNN- KNeighborsClassifier Model 
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5) # How many neighbors we want to take
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix:\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy :",ac)

# 06 naive_bayes / GaussianNB Model
X = full_data.iloc[:,0:13].values
y = full_data.iloc[:,13].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) # it keeps the value in a range
X_test = sc_X.fit_transform(X_test)


from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix:\n",cm)
ac = accuracy_score(y_test,y_pred)
print("Accuracy :",ac)