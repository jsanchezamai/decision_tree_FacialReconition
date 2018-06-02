import math
import random
import numpy as np
# Tree class is the node in our decesion tree, including information about:
#   op: attribute of this node
#   cls: 1 or 0 which only exsits in leaf node
#   kids: two kid nodes of current node, kids[0]: false kids[1] : true
class Tree:
    def __init__(self):
        self.op = None
        self.kids = []
        self.cls = None
    def setOp(self, attribute):
        self.op = attribute
    def set_leaf(self, value):
        self.cls = value
    def set_kids(self, left_tree, right_tree):
        self.kids.append(left_tree)
        self.kids.append(right_tree)
    def get_max_depth(self):
        if self.op == None:
            return 1
        return max(1+self.kids[0].get_max_depth(), 1+self.kids[1].get_max_depth())
#define functions-----------------------------------------------------------
        
# train_tree returns the root node given data, targets and emotion
def train_tree(examples, targets, emotion_label):
    binary_targets = get_binary(targets, emotion_label)
    examples, binary_targets = data_preprocess(examples, binary_targets)
    attributes = list(np.arange(0, 45))
    return decision_tree_learning(examples,attributes,binary_targets)

# choose_best_attribute returns attribute with highest information gain given data
def choose_best_attribute(examples, attributes, binary_targets):
    max_gain = -1
    max_attributes = []   
    #for each attribute, calculate its p,n,p0,n0,p1,n1
    for i in range(0, len(attributes)):
        p = 0; n = 0; p0 = 0; n0 = 0; p1 = 0; n1 = 0;   
        # calculate positive numbers and negative numbers
        # and them for each posibie attribute subset and negative attribute subset
        for j in range(0, len(binary_targets)):
            if(binary_targets[j] == 1):
                p+=1
            if(binary_targets[j] == 0):
                n+=1
            if(binary_targets[j] == 1 and examples[j][attributes[i]] == 0):
                p0+=1
            if(binary_targets[j] == 0 and examples[j][attributes[i]] == 0):
                n0+=1
            if(binary_targets[j] == 1 and examples[j][attributes[i]] == 1):
                p1+=1
            if(binary_targets[j] == 0 and examples[j][attributes[i]] == 1):
                n1+=1
        Remainder = (p0+n0)/(p+n) * I(p0,n0) + (p1+n1)/(p+n) * I(p1,n1)
        Gain = I(p,n) - Remainder
        # in case there are two or more attributes having same information gain
        # we store highest attributes in the array
        if(Gain > max_gain):
            max_attributes = []
            max_attributes.append(attributes[i])
            max_gain = Gain
        elif(Gain == max_gain):
            max_attributes.append(attributes[i])
    # pick first attributes in highest attributes array (actually we can also choose to pick randomly)
    return max_attributes[0], max_gain
    
# majority value of targets
def majority_value(binary_targets):
	value0 = binary_targets.count(0)
	value1 = binary_targets.count(1)
	return (0 if value0 > value1 else 1)

# divide targets into positive ones and negatives ones according to the emotional label
def get_binary(targets, emotion_label):
    results = list(map(lambda x : 1 if x == emotion_label else 0, targets))
    return results
              
# calculate information gain 
def I(p,n):
    if(p != 0 and n != 0):
        return (-float(p)/(p+n)) * math.log(float(p)/(p+n),2) - (float(n)/(p+n)) * math.log(float(n)/(p+n),2)
    if(p == 0 or n == 0):
        return 0

# divide data into two sets according to the value of best attribute
def sift(best_attribute, value, examples, binary_targets):
    examples_si = []
    binary_targets_si = []
    for i in range(0, len(examples)):
        if(examples[i][best_attribute] == value):
            examples_si.append(examples[i])
            binary_targets_si.append(binary_targets[i])
    return (examples_si, binary_targets_si)



# decision_tree_learning returns the root node given training data
def decision_tree_learning(examples,attributes,binary_targets):
    tree = Tree()
    if small_entropy(binary_targets, 0.2): 
        #print('come here') 
        tree.set_leaf(majority_value(binary_targets)) 
        return tree 
    # if all examples have the same value of binary_targets return a leaf node with this value
    if(binary_targets.count(binary_targets[0]) == len(binary_targets)):
        tree.set_leaf(binary_targets[0])
        return tree
    
    # if attributes is empty return a leaf node with majority value
    if(len(attributes) == 0):
        tree.set_leaf(majority_value(binary_targets))
        return tree
    
    # choose the best value which has highest information gain
    best_attribute, max_gain = choose_best_attribute(examples, attributes, binary_targets)
  
    attributes_copy = attributes[:]
    attributes_copy.remove(best_attribute)
    
    # devide examples and targets into two subsets according to current attrubute
    (examples_s0,binary_targets_s0) = sift(best_attribute,0,examples,binary_targets)
    (examples_s1,binary_targets_s1) = sift(best_attribute,1,examples,binary_targets)
    
    #if example is empty return a leaf node with majority value
    if(len(examples_s0) == 0):
        tree.set_leaf(majority_value(binary_targets_s1))
        return tree
    elif(len(examples_s1) == 0):
        tree.set_leaf(majority_value(binary_targets_s0))
        return tree
    
    #find two kid nodes of currentnodes
    else:
        tree.setOp(best_attribute)
        tree.set_kids(decision_tree_learning(examples_s0, attributes_copy, binary_targets_s0),
                      decision_tree_learning(examples_s1, attributes_copy, binary_targets_s1))
        return tree


def data_preprocess(examples, binary_targets):
    data_map = {}
    delete_index = []
    for index in range(len(examples)):
        if tuple(examples[index]) not in data_map:
            data_map[tuple(examples[index])] = [index]
        else:
            data_map[tuple(examples[index])].append(index)
    for key,value in data_map.items():
        if len(value)>1:
            modify_data(examples, binary_targets, value, delete_index)
    binary_targets = [binary_targets[index] for index in range(len(binary_targets)) if index not in delete_index]
    examples = [examples[index] for index in range(len(examples)) if index not in delete_index]
    return examples, binary_targets
    
            

def modify_data(examples, binary_targets, index_lst, delete_index):
    target_lst = [binary_targets[index] for index in index_lst]
    count_0 = target_lst.count(0)
    count_1 = target_lst.count(1)
    value = 0 if count_0 > count_1 else 1
    if I(count_0, count_1)>0.92:
        delete_index += index_lst
    else:
        for index in index_lst:
            binary_targets[index] = value


def small_entropy(binary_targets, threshold = 0.1):
    count_0 = binary_targets.count(0)
    count_1 = binary_targets.count(1)
    return I(count_0, count_1) < threshold
        
        
        

