'''
Created on Aug 25, 2016
This class is a decision tree implementation taken from Hal Daume.

@author: km_dh
'''

import numpy as np
from scipy import stats

class DT(object):
    '''
    classdocs TODO: Fill this in
    '''   
    def __init__(self):
        '''
        constructor
        '''
        
    def res(self,mode='name', model={}, test_case=np.zeros(1), X=np.zeros(1), Y=np.zeros(1), h_param=1):
        '''
        usage is of the two following:
        learn = DT()
        model = learn.res('train', X=, Y=, cutoff=)
        Y = learn.res('predict', model=, X=)
        '''
        mode = mode.lower()
        
        if(mode == 'name'):
            return 'DT'
        
        if(mode == 'train'):
            if(len(X) < 2 or len(Y) < 1 or h_param < 0):
                print("Error: training requires three arguments: X, Y")
                return 0
            sizeX = X.shape
            sizeY = Y.shape
            if(sizeX[0] != sizeY[0]):
                print("Error: there must be the same number of data points in X and Y")
                return 0
            if sizeY[1] != 1:
                print("Error: Y must have only 1 column")
                return 0
            if(h_param not in range(1000)):
                print("Error: cutoff must be a positive scalar")
                return 0
            res = {}
            res = self.DTconstruct(X,Y,h_param)
            return res
        
        if(mode == 'predict'):
            if(len(model) < 1 or len(test_case) < 1):
                print("Error: prediction requires two arguments: the model and X")
                return 0
            if('isLeaf' not in model.keys()):
                print("Error: model does not appear to be a DT model")
                return 0
            
            #set up output
            rowCol = test_case.shape
            if(len(rowCol) < 2):
                res = self.DTpredict(model, test_case)
            else:
                N = rowCol[0]
                res = np.zeros(N)
                for n in range(N):
                    ans = self.DTpredict(model, test_case[n,:])
                    res[n] = ans
            return res
        print("Error: unknown DT mode: need train or predict")
        
    
       
    def DTconstruct(self,X,Y,cutoff):
        # the Data comes in as X which is NxD and Y which is Nx1.
        # cutoff is a scalar value. We should stop splitting when N is <= cutoff
        #
        # features (X) may not be binary... you should *threshold* them at
        # 0.5, so that anything < 0.5 is a "0" and anything >= 0.5 is a "1"
        #
        # we want to return a *tree*. the way we represent this in our model 
        # is that the tree is a Python dictionary.
        #
        # to represent a *leaf* that predicts class 3, we can say:
        #    tree = {}
        #    tree['isLeaf'] = 1
        #    tree['label'] = 3
        #
        # to represent a split node, where we split on feature 5 and then
        # if feature 5 has value 0, we go down the left tree and if feature 5
        # has value 1, we go down the right tree.
        #    tree = {}
        #    tree['isLeaf'] = 0
        #    tree['split'] = 5
        #    tree['left'] = ...some other tree...
        #    tree['right'] = ...some other tree...

        fRow, fCol = X.shape

        tree = {}
        maxScore = -1
        classes = np.unique(Y)
        guess = 0 if len(Y) < 1 else stats.mode(Y)[1][0]
        if len(Y) < 1 or len(classes)==1 or fCol < 1 or fRow <= cutoff:  # check if labels are unambigous

            tree['isLeaf'] = 1
            tree['label'] = guess
            return tree

        else:  # for all remaining features
            #unique_labels = list(set(Y))
            for col in range(fCol):
                labelNo = Y[np.where(X[:, col] == 0)]
                if len(labelNo) < 1:
                    noCountMax = [[0],[0]]
                else:
                    noCountMax = stats.mode(labelNo)

                labelYes = Y[np.where(X[:, col] == 1)]
                if len(labelYes) < 1:
                    yesCountMax = [[0],[0]]

                else:
                    yesCountMax = stats.mode(labelYes)


                currentScore = noCountMax[1][0] + yesCountMax[1][0]
                if (currentScore > maxScore):
                    maxScore = currentScore
                    maxIndex = col



            noArray = X[np.where(X[:, maxIndex] <0.5)]
            labelNo = Y[np.where(X[:, maxIndex] <0.5)]
            yesArray = X[np.where(X[:, maxIndex] >=0.5)]
            labelYes = Y[np.where(X[:, maxIndex] >=0.5)]

            noArray=np.delete(noArray, maxIndex, axis=1)
            yesArray=np.delete(yesArray, maxIndex, axis=1 )

            tree['isLeaf'] = 0
            tree['split'] = maxIndex
            tree['left'] = self.DTconstruct(noArray, labelNo, cutoff)
            tree['right'] = self.DTconstruct(yesArray, labelYes, cutoff)
            return tree


    def DTpredict(self,model,X):
        # here we get a tree (in the same format as for DTconstruct) and
        # a single 1xD example that we need to predict with


       #if( model['isLeaf'] == 0):
           # return 9999

        if(model['isLeaf'] == 1):
            return model['label']

        split = model['split']
        if(X[split] <0.5):
            X=np.delete(X,split)
            return  self.DTpredict(model['left'], X)
        else:
            X= np.delete(X,split)
            return self.DTpredict(model['right'], X)


    def DTdraw(self,model,level=0):
        indent = ' '
        if model is None:
            return
        print indent*4*level + 'isLeaf: ' + str(model['isLeaf'])
        if model['isLeaf']==1:
            print indent*4*level + 'Y: ' + str(model['label'])
            return
        print indent*4*level + 'split ' + str(model['split'])
        left_tree = str(self.DTdraw(model['left'],level+1))
        if left_tree != 'None':
            #print model['left']
            print indent*4*level + 'left: ' + left_tree
        right_tree = str(self.DTdraw(model['right'],level+1))
        if right_tree != 'None':
            #print model['right']
            print indent*4*level + 'right: ' + right_tree
        
