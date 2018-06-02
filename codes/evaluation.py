from random import choice
from numpy import arange, array
import matplotlib.pyplot as plt
import numpy as np

#This function accepts one tree class and one feature example 
#and returns the pridicted label
def predict(tree, example):
    attri = tree.op
    left_node = tree.kids[0]
    right_node = tree.kids[1]
    if (example[attri] == 0):
        if left_node.op == None:#left_node is a leave node
            return left_node.cls
        else:#left_node is a root node
            return predict(left_node, example)
    else:
        if right_node.op == None:
            return right_node.cls
        else:
            return predict(right_node, example)
#This function accepts a group of tree class and a list of feature examples
#and return a list of prediceted labels for corresponding example 

def testTrees(trees, examples):
    predictions = []
    matched = []
    for example in examples:
        max_depth = 0
        max_index = 0
        matched = []
        for index in range(len(trees)):
            if predict(trees[index], example) == 1:
                matched.append(index+1)#store all matched labels in a list
        if len(matched) == 0:#No matched label found
            predictions.append(1+choice(arange(len(trees))))#randomly choose a label
        else:
            predictions.append(choice(matched))
    return array(predictions)
#This function accepts two list of data, one represents the expected results and the other
#represent the predicted ones. 
def getConfusionMat(expected, predictions):
    new_expected = expected.flatten()
    confusion_mat = [array([0]*6) for i in range(6)]
    for index in range(len(predictions)):
        if predictions[index] == new_expected[index]:
            confusion_mat[new_expected[index]-1][new_expected[index]-1] += 1
        else:
            confusion_mat[new_expected[index]-1][predictions[index]-1] += 1
    return confusion_mat
#Find the F1 value according to the confusion matrix
def calFAlpha(confusion_mat):
    FAlpha = []
    for index in range(6):
        tp = confusion_mat[index][index]
        fn = sum(confusion_mat[index]) - tp
        fp = sum([i[index] for i in confusion_mat]) - tp
        recall_rate = tp/float(tp+fn)
        precision_rate = tp/float(tp+fp)
        print(index+1, "recall: ", round(recall_rate, 3), "  precission: ", round(precision_rate, 3))
        if recall_rate*precision_rate == 0:
            FAlpha.append(0)
        else:
            FAlpha.append(2*precision_rate*recall_rate/(precision_rate+recall_rate))
    return array(FAlpha)

#Function accepts a 2-dimension matrix and visualize it 
def visualizaConfusMat(confusion_mat):
	data = [[i for i in entry] for entry in confusion_mat]
	rows = columns = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
	n_rows = len(data)
	max_value = float(max([max(entry) for entry in data]))
	cell_color = [[[0, 0.5, 0.9, 0.5/max_value*i+0.5] for i in entry] for entry in data]
	cell_text = [[str(i) for i in entry] for entry in data]

	column_header = plt.table(cellText=[['Prediction']],
	                   cellLoc = 'center',
	                   loc='bottom left', bbox = [-0.1, 0, 1.2, 0.3])             
	column_header.set_fontsize(24)
	the_table = plt.table(cellText=cell_text,
	                      cellColours = cell_color,
	                      rowLabels=rows,
	                      rowLoc = 'center',
	                      cellLoc = 'center',
	                      colWidths = [0.2]*n_rows,
	                      colLabels=columns,
	                      loc='bottom')
	the_table.scale(1,6)
	the_table.set_fontsize(34)
	plt.axis('off')
	plt.show()

def calError(expected, predictions):
    error = 0
    new_exp = expected.flatten()
    for index in range(len(new_exp)):
        if new_exp[index] != predictions[index]:
            error += 1
    error /= len(new_exp)
    return error
        
def sample_classfication(targets):
    new_target = targets.flatten()
    label_count = {};
    for label in new_target:
        if label_count.get(label, 0)==0:
            label_count[label] = 1
        else:
            label_count[label] += 1
    return label_count
        
        



