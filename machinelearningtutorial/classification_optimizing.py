import numpy as np
from sklearn import cross_validation, datasets, svm
digits = datasets.load_digits()
X = digits.data
y = digits.target
svc = svm.SVC(kernel='linear')
C_s = np.logspace(-10, 0, 10)
scores = list()
scores_std = list()
for C in C_s:
	svc.C = C
	this_scores = cross_validation.cross_val_score(svc, X, y, n_jobs=1)
	scores.append(np.mean(this_scores))
	scores_std.append(np.std(this_scores))

print(scores)
