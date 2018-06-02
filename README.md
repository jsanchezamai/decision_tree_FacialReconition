# Decision tree algorithm on facial expression recognition
This is the simple decision tree algorithm on distinguishing between six basic facial recognition (anger, disgust, fear, happiness, sadness and surprise) based on a labelled set of facial Action Units (AUs).

**The data is as follows:**
**Input data** :  A matrix x, which is an N×45 matrix, where N is the total number of examples and 45 is the total number of AUs that can be activated or not. In case an AU is activated, the value of the corresponding column will be 1. Otherwise, it will be 0. For instance, the following row 
[1 1 0 0 1 0 …0]
would mean that AU1, AU2 and AU5 are activated.
**Output data:**  A vector y of dimensions N×1, containing the emotion labels of the corresponding examples. These labels are numbered from 1 to 6, and correspond to the emotions anger, disgust, fear, happiness, sadness and surprise respectively.

trees.pkl is the combination of our 6 trees of 6 emotions we have trained on the entire clean dataset.

To use it, just as following:

    pkl_file = open('trees.pkl', 'rb')
    trees = pickle.load(pkl_file)
    prediction = testTrees(trees, data)

where data is the test data, trees is the list of 6 trees. testTrees function is in our evaluation.py


**#Explanation of our other functions**
1. To train data, there's a function in trainTrees.py:

    train_tree(examples, targets, emotion_label)

where examples is training data, targets is training target, emotion_label is from 0 to 6. It will return the tree

2. To make prediction:

    prediction = testTrees(trees, data)

where data is the test data, trees is the list of 6 trees. it will return the list of prediction labels.

3. To visualize the tree:

    visual_tree(tree)

where tree is one specific tree
