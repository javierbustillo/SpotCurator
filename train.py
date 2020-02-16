import numpy
from joblib import dump
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

target = []
data = []
with open('features.csv') as data_file:
    dat = data_file.read().splitlines()
    print(len(dat))
    for datum in dat:
        split_datum = datum.split(',')
        data.append([float(split) for split in split_datum[:-1]])
        target.append(split_datum[-1])
X_train, X_test, y_train, y_test = train_test_split(numpy.array(data), numpy.array(target))
logistic_regression = LogisticRegression(C=100).fit(X_train, y_train)
print('accuracy train: %f' % logistic_regression.score(X_train, y_train))
print('accuracy on test: %f' % logistic_regression.score(X_test, y_test))
dump(logistic_regression, 'recommender.joblib')
