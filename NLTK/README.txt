*files we used for our analysis with Python NLTK
*Future_Predictions contains predictions for stock movement based on training.
*regNER.py generates featuresets, it is the program that actually uses NLTK
*combined_learn2.py trains the data with a voted classifier. Multiple classifiers are implemented: MNB_classifier, BernoulliNB_classifier, RandomForest_classifier, LogisticRegression_classifier, SGDClassifier_classifier, SVC_classifier, and LinearSVC_classifier.
*PredictNew.py uses the news data from the last 2 days and predicts 3 days ahead, so it predicts tomorrow and the day after that.
