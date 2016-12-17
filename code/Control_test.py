'''
Created on Sept 19, 2016

@author: km_dh
'''
import numpy as np
import DT as dt
import KNN as knn


if __name__ == '__main__':

    print 'running tests on DT and KNN'
    #This is the class example [mathy, test >= 80, project >= 80, early]
    #with a slight change so that non-mathy first splits on early.
    trX=np.array([[1,1,1,1],[1,1,1,0],[0,1,0,1],[0,0,1,1],[0,0,1,1],[0,0,0,0],[0,0,0,0],[1,0,1,1],[1,0,0,1],[0,0,1,1],[1,0,0,0],[0,0,1,1],[0,1,0,1],[0,0,1,0]])
    trY=np.array([[1],[1],[0],[0],[0],[1],[0],[1],[0],[0],[0],[0],[0],[1]])
    deX = np.array([[0,1,0,0],[0,0,1,0],[0,1,1,1]])
    deY = np.array([[0],[1],[0]])

    decTree = dt.DT()
    print 'DT, cutoff=0'
    trainModel = decTree.res('train',X=trX,Y=trY,h_param=0)
    decTree.DTdraw(trainModel)
    output = decTree.res('predict',model=trainModel,test_case=deX)
    print output
    
    knnMode = knn.KNN()
    print 'KNN, k=1'
    trainModel = knnMode.res('train',X=trX,Y=trY,h_param=1)
    output = knnMode.res('predict',model=trainModel,test_case=deX)
    print output
    
    print 'Done'
