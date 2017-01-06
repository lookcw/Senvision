from nltk.corpus import names
def gender_features(word):
     return {'last_letter': word[-1]}

labeled_names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in names.words('female.txt')])
import random
random.shuffle(labeled_names)
featuresets = [(	gender_features(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]
print train_set
classifier = nltk.NaiveBayesClassifier.train(train_set)