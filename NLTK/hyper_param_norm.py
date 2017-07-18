import optunity
import optunity.metrics
import numpy as np
import csv
# k nearest neighbours
from sklearn.neighbors import KNeighborsClassifier
# support vector machine classifier
from sklearn.svm import SVC
# Naive Bayes
from sklearn.naive_bayes import GaussianNB
# Random Forest
from sklearn.ensemble import RandomForestClassifier

from sklearn.datasets import load_digits


def train_svm(data, labels, kernel, C, gamma, degree, coef0):
    """A generic SVM training function, with arguments based on the chosen kernel."""
    if kernel == 'linear':
        model = SVC(kernel=kernel, C=C)
    elif kernel == 'poly':
        model = SVC(kernel=kernel, C=C, degree=degree, coef0=coef0)
    elif kernel == 'rbf':
        model = SVC(kernel=kernel, C=C, gamma=gamma)
    else:
        raise ArgumentError("Unknown kernel function: %s" % kernel)
    model.fit(data, labels)
    return model

search = {'algorithm': {'k-nn': {'n_neighbors': [1, 5]},
                        'SVM': {'kernel': {'linear': {'C': [0, 2]},
                                           'rbf': {'gamma': [0, 1], 'C': [0, 10]},
                                           'poly': {'degree': [2, 5], 'C': [0, 50], 'coef0': [0, 1]}
                                           }
                                },
                        'naive-bayes': None,
                        'random-forest': {'n_estimators': [10, 30],
                                          'max_features': [5, 20]}
                        }
         }



with open('test4.csv', 'rb') as f:
    reader = csv.reader(f)
    digits = list(reader)
    digits=np.array(digits)
n = len(digits)

positive_digit = 1
negative_digit = 0
HC_idx=[]
AD_idx=[]
print digits
print n


for i in range(len(digits)):
    if digits[i][-1]=="1":
        AD_idx.append(i)
    if digits[i][-1]=="0":
        HC_idx.append(i)


print AD_idx

# add some noise to the data to make it a little challenging

data=digits
labels = [1] * len(AD_idx) + [0] * len(HC_idx)
print labels
@optunity.cross_validated(x=data, y=labels, num_folds=10)
def performance(x_train, y_train, x_test, y_test,
                algorithm, n_neighbors=None, n_estimators=None, max_features=None,
                kernel=None, C=None, gamma=None, degree=None, coef0=None):
    # fit the model
    if algorithm == 'k-nn':
        model = KNeighborsClassifier(n_neighbors=int(n_neighbors))
        model.fit(x_train, y_train)
    elif algorithm == 'SVM':
        model = train_svm(x_train, y_train, kernel, C, gamma, degree, coef0)
    elif algorithm == 'naive-bayes':
        model = GaussianNB()
        model.fit(x_train, y_train)
    elif algorithm == 'random-forest':
        model = RandomForestClassifier(n_estimators=int(n_estimators),
                                       max_features=int(max_features))
        model.fit(x_train, y_train)
    else:
        raise ArgumentError('Unknown algorithm: %s' % algorithm)

    # predict the test set
    if algorithm == 'SVM':
        predictions = model.decision_function(x_test)
    else:
        predictions = model.predict(x_test)
    print x_test
    print x_train
    print predictions
    print y_test
    print "__________"
    return optunity.metrics.accuracy(y_test,predictions)
    #return optunity.metrics.roc_auc(y_test, predictions, positive=True)






print performance(algorithm='random-forest',n_estimators=100,max_features=100)
# optimal_configuration, info, _ = optunity.maximize_structured(performance,
#                                                                search_space=search,
#                                                                num_evals=300)


# print(optimal_configuration)
# print(info.optimum)