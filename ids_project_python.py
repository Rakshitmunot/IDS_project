# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as TTS
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

df=pd.read_csv("letter-recognition.data")
print(df)

df.shape

df

df['letter'].value_counts()

df.isnull().sum()

df.describe()

Train,  Test=TTS(df,test_size=0.2,random_state=4)

Train

Train.shape

Test

Test.shape

X_train=Train.drop(['letter'],axis=1)

X_train.head()

T_train=Train['letter']

T_train.head()

X_test=Test.drop(['letter'],axis=1)

X_test.head()

T_test=Test['letter']

T_test.head()

"""# Normalisation of Training and Test Data

# 1.Standard Scaling
"""

scaled_X = StandardScaler().fit_transform(X_train.values)

X_train_ss = pd.DataFrame(scaled_X, index = X_train.index, columns = X_train.columns)

X_train_ss.describe()

"""# 2. Min-Max Scaling"""

scaled_train = MinMaxScaler().fit_transform(X_train.values)

X_train_s = pd.DataFrame(scaled_train, index = X_train.index, columns=X_train.columns)

X_train_s.describe()

scaled_test=MinMaxScaler().fit_transform(X_test.values)

X_test_s=pd.DataFrame(scaled_test, index=X_test.index, columns=X_test.columns)

X_test_s.describe()

"""# Different Kinds of Plots"""

df['letter'].value_counts().plot(kind='bar')

T_train.value_counts().plot(kind='bar')

T_test.value_counts().plot(kind='bar')

"""# In further proceeding we will calculate influence of each attribute on Letter in ascending order and drop the least important attribute(s)"""

att_fig, (ax) = plt.subplots(4, 4, figsize=(30,30))
att_fig.suptitle('Sharing attributes(x) per letter(y)', fontsize=30)

#x-box
ax[0,0].scatter(X_train_s['x-box'], T_train)
ax[0,0].set_title('X-Box', fontsize=18)

#y-box
ax[0,1].scatter(X_train_s['y-box'], T_train)
ax[0,1].set_title('Y-box', fontsize=18)

#width
ax[0,2].scatter(X_train_s['width'], T_train)
ax[0,2].set_title('Width', fontsize=18)

#high
ax[0,3].scatter(X_train_s['high'], T_train)
ax[0,3].set_title('High', fontsize=18)

#onpix
ax[1,0].scatter(X_train_s['onpix'], T_train)
ax[1,0].set_title('Onpix', fontsize=18)

#x-bar
ax[1,1].scatter(X_train_s['x-bar'], T_train)
ax[1,1].set_title('X-bar', fontsize=18)

#y-bar
ax[1,2].scatter(X_train_s['y-bar'], T_train)
ax[1,2].set_title('Y-bar', fontsize=18)

#x2bar
ax[1,3].scatter(X_train_s['x2bar'], T_train)
ax[1,3].set_title('X2Bar', fontsize=18)

#y2bar
ax[2,0].scatter(X_train_s['y2bar'], T_train)
ax[2,0].set_title('Y2Bar', fontsize=18)

#xybar
ax[2,1].scatter(X_train_s['xybar'], T_train)
ax[2,1].set_title('XY Bar', fontsize=18)

#x2ybr
ax[2,2].scatter(X_train_s['x2ybr'], T_train)
ax[2,2].set_title('X2YBr', fontsize=18)

#xy2br
ax[2,3].scatter(X_train_s['xy2br'], T_train)
ax[3,3].set_title('XY2Br', fontsize=18)

#x-ege
ax[3,0].scatter(X_train_s['x-ege'], T_train)
ax[3,0].set_title('X-Ege', fontsize=18)

#xegvy
ax[3,1].scatter(X_train_s['xegvy'], T_train)
ax[3,1].set_title('Xegvy', fontsize=18)

#y-ege
ax[3,2].scatter(X_train_s['y-ege'], T_train)
ax[3,2].set_title('Y-ege', fontsize=18)

#yegvx
ax[3,3].scatter(X_train_s['yegvx'], T_train)
ax[3,3].set_title('Yegvx', fontsize=18)

from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()
model.fit(X_train_s,T_train)
print(model.feature_importances_)
feat_importances = pd.Series(model.feature_importances_, index=X_train_s.columns)
feat_importances.nlargest(16).plot(kind='barh')
plt.show()

"""# SVM Classifier :-"""

from sklearn import metrics
from sklearn import svm
clf = svm.SVC(kernel='linear')
clf.fit(X_train_s,T_train)
T_pred = clf.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred, average='weighted')))

"""# F-beta Score

"""

from sklearn.metrics import fbeta_score
print(fbeta_score(T_test, T_pred,average='weighted', beta=1))

"""# Naive Bayes Classifier:-

"""

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train_s, T_train)
T_pred_nb = gnb.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred_nb, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred_nb)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred_nb, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred_nb, average='weighted')))

"""# F-Beta Score"""

print(fbeta_score(T_test, T_pred_nb,average='weighted', beta=1))

"""# Random Forest Classifier :-"""

from sklearn.ensemble import RandomForestClassifier
clf_r = RandomForestClassifier(max_depth=16, random_state=0)
clf_r.fit(X_train_s,T_train)
T_pred_rf = clf_r.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred_rf, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred_rf)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred_rf, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred_rf, average='weighted')))

"""

```
# This is formatted as code
```

# F-Beta Score"""

print(fbeta_score(T_test, T_pred_rf,average='weighted', beta=1))

"""# K-Nearest Neighbors"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
knn_clf = KNeighborsClassifier(n_neighbors=7)
knn_clf.fit(X_train_s, T_train)
T_pred_knn = knn_clf.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred_knn, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred_knn)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred_knn, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred_knn, average='weighted')))

"""# F-Beta Score"""

print(fbeta_score(T_test, T_pred_knn,average='weighted', beta=1))

"""# Decision Tree"""

from sklearn.tree import DecisionTreeClassifier
dt_clf = DecisionTreeClassifier()
dt_clf.fit(X_train_s, T_train)
T_pred_dt = dt_clf.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred_dt, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred_dt)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred_dt, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred_dt, average='weighted')))

"""# F-Beta Score"""

print(fbeta_score(T_test, T_pred_dt,average='weighted', beta=1))

"""# Logistic Regression"""

from sklearn.linear_model import LogisticRegression
clf_lr = LogisticRegression(max_iter=10000,random_state=0)
clf_lr.fit(X_train_s, T_train)
T_pred_lr = clf_lr.predict(X_test_s)

df = pd.DataFrame(metrics.confusion_matrix(T_pred_lr, T_test))
df

print('Accuracy: {:.5f}'.format(metrics.accuracy_score(T_test, T_pred_lr)))
print('Precision: {:.5f}'.format(metrics.precision_score(T_test, T_pred_lr, average='weighted')))
print('Recall: {:.5f}'.format(metrics.recall_score(T_test, T_pred_lr, average='weighted')))

"""# F-Beta Score"""

print(fbeta_score(T_test, T_pred_lr,average='weighted', beta=1))

