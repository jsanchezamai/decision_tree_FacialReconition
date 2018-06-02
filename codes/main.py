#Python version: Python 3
import numpy as np
from evaluation import *
from visualization import *
from trainTrees import *
import scipy.io as spio
#Loading data from file
data = spio.loadmat('cleandata_students.mat')


# begin 10-fold validation to compute confusion matrix and all evaluations
examples = data["x"]
targets = data["y"]
confusion_mat = np.zeros(shape=(6,6))
error_sum = 0
for fold_index in range(10):#10-fold validation
    trees = []
    #Catagory the training data and testing data
    test_data_index = 100 * fold_index
    test_data = examples[test_data_index:test_data_index+100]
    test_target = targets[test_data_index:test_data_index+100]
    training_data = np.append(examples[:test_data_index],examples[test_data_index+100:], axis = 0)
    training_target = np.append(targets[:test_data_index],targets[test_data_index+100:], axis = 0)
 
    #Training for trees of 6 labels
    for index in range(6):
        tree = train_tree(training_data, training_target, index+1)
        trees.append(tree) 
    prediction = testTrees(trees, test_data) 
    cm = getConfusionMat(test_target, prediction)
    confusion_mat += cm
    error = calError(test_target, prediction)
    error_sum += error    
print("\n\n****************************") 
print("Average information report")  
print("****************************")
confusion_mat /= 10
visualizaConfusMat(confusion_mat)
Fa = calFAlpha(confusion_mat)
print('\nfa: ', Fa) 
print("\nThe classification rate: "+str(1-error_sum/10))


# visulize tree (just need to input the root node of the tree)
# Here just choose the first tree as example
visual_tree(trees[0])



