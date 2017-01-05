import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm
import datetime
import csv
import sys

descriptor_dir = '../CorrelationAnalysis/newsdescriptors/'	
results_file=open('../Results/sklearn_results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
n = 1
identifier="default identifier"
for argument in sys.argv[1:]:
	if argument == "-iden":
		identifier = sys.argv[n+1]
	n+=1
	
if identifier == "default identifier":
	print "error: put in identifier with -iden arg"
	sys.exit(0)
now = datetime.datetime.now()
if identifier!="0":
	result_writer.writerow([now,identifier])


for subdir, dirs, files in os.walk(descriptor_dir):
    for file in files:
	des_file=open(os.path.join(subdir, file),'r')
	reader=csv.reader(des_file,delimiter='\t')
	array=np.array(list(reader))
	print array.shape
	comp_name=array[1][1]
	array=array[1:]#take out company names names
	data=array[:][:,2:-2] #extract the training data without target
	target=array[:][:,-2] #extract target
	elements=len(data)
	for i in range(0,num_folds):
		first_index=(i*float(elements)/num_folds)
		second_index=((i+1)*float(elements)/num_folds)
		test_data = data[first_index:second_index]
		train_data= list(set(data[0:first_index]).union(set(data[second_index[second_index:]])))
		train_target= list(set(target[0:first_index]).union(set(target[second_index[second_index:]])))
		print (len(train_data)+len(test_data))," ",len(data)
	if identifier!="0":
		result_writer.writerow([comp_name,metrics.accuracy_score(target,predicted)])
	print comp_name+ ": "+ str(metrics.accuracy_score(target,predicted))
	

