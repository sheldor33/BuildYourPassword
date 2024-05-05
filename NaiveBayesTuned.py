import pandas as pd
import numpy as np

import time

# For text feature extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# For creating a pipeline
from sklearn.pipeline import Pipeline

# Classifier Model (Naive Bayes)
from sklearn.naive_bayes import BernoulliNB

# To save the trained model on local storage
import joblib

# Read the File
data = pd.read_csv('data.csv')

# Features which are passwords
features = data.values[:, 1].astype('str')

# Labels which are strength of password
labels = data.values[:, -1].astype('int')

classifier_model = Pipeline([
                ('tfidf', TfidfVectorizer(analyzer='char')),
                ('bernoulliNB',BernoulliNB()),
])

vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(1,2))
vectorized=vectorizer.fit_transform(features)
all_ngrams = vectorizer.get_feature_names()
# display top min(50,len(all_ngrams) of the most frequent words
num_ngrams = min(50, len(all_ngrams))

# count the number of words in the total corpse
all_counts = vectorized.sum(axis=0).tolist()[0]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(features,labels,test_size=0.20,random_state=0)
X_train=vectorizer.fit_transform(X_train)
X_test=vectorizer.transform(X_test)

start_time = time.time()
classifier_model=BernoulliNB(alpha=0.0172727)
classifier_model.fit(X_train,y_train)
y_pred = classifier_model.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report
cm=confusion_matrix(y_test,y_pred)
print(classification_report(y_test, y_pred, digits=4))
print("Confusion Matrix: \n", cm)
accuracy = (cm[0][0]+cm[1][1]+cm[2][2])/(cm[0][0]+cm[0][1]+cm[0][2]+cm[1][0]+cm[1][1]+cm[1][2]+cm[2][0]+cm[2][1]+cm[2][2])
print('Training Accuracy: ',classifier_model.score(features, labels))
print("Testing Accuracy = ", accuracy)
print("Time Taken to train the model = %s seconds" % round((time.time() - start_time),2))
joblib.dump(classifier_model, 'NaiveBayes_ModelTuned.joblib')