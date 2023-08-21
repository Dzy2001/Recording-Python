import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',None)

#The resultant data for each category will be saved in Excel format.
#Different types of indicators are positively oriented in different ways.
#This requires you to define one or more simple functions to positively orient one or more indicators.
#Of course, this needs to be done in advance.

class EWM:
    
    def __init__(self, info):
        self.info = info
        self.index = info.index
        self.columns = info.columns
        self.lrows = len(info.index)
        self.lcolumns = len(info.columns)
        
    def Regularization(self):
        pass
    
    def Normalization(self):
        self.ndata = pd.DataFrame(np.zeros((self.lrows, self.lcolumns)))
        self.ndata.index = self.index
        self.ndata.columns = self.columns
        for c in np.arange(self.lcolumns):
            for r in np.arange(self.lrows):
                self.ndata.iloc[r, c] = (self.info.iloc[r, c] - self.info.iloc[:, c].min()) / (self.info.iloc[:, c].max() - self.info.iloc[:, c].min())
        self.ndata.to_excel('ndata_ewm.xlsx')
    
    def sNormalization(self):
        self.ndata = pd.DataFrame(np.zeros((self.lrows, self.lcolumns)))
        self.ndata.index = self.index
        self.ndata.columns = self.columns
        self.sndata = pd.DataFrame(np.zeros((1, self.lcolumns)))
        for c in np.arange(self.lcolumns):
            sx2 = 0
            for r in np.arange(self.lrows):
                sx2 += self.info.iloc[r, c]**2
            self.sndata.iloc[0, c] = np.sqrt(sx2)
            
        for c in np.arange(self.lcolumns):
            for r in np.arange(self.lrows):
                self.ndata.iloc[r, c] = self.info.iloc[r, c] / self.sndata.iloc[0, c]
        self.ndata.to_excel('ndata_ewm_xij.xlsx'); self.sndata.to_excel('sndata_ewm_xij.xlsx')
    
    def getPmatrix(self):
        self.pmatrix = pd.DataFrame(np.zeros((self.lrows, self.lcolumns)))
        self.pmatrix.index = self.index
        self.pmatrix.columns = self.columns
        for c in np.arange(self.lcolumns):
            for r in np.arange(self.lrows):
                self.pmatrix.iloc[r, c] = self.ndata.iloc[r, c] / self.ndata.iloc[:, c].sum()
        self.pmatrix.to_excel('pmatrix.xlsx')
        
    def dealPmatrix(self):
        self.dmatrix = pd.DataFrame(np.zeros((self.lrows, self.lcolumns)))
        self.dmatrix.index = self.index
        self.dmatrix.columns = self.columns
        for r in np.arange(self.lrows):
            for c in np.arange(self.lcolumns):
                self.dmatrix.iloc[r, c] = self.pmatrix.iloc[r, c] * np.log(self.pmatrix.iloc[r, c])
        self.dmatrix.to_excel('dmatrix.xlsx')
                
    def getInfoentropy(self):
        self.k = -1/np.log(self.lcolumns)
        self.entropy = pd.DataFrame(np.zeros((1, self.lcolumns)))
        self.entropy.index = ['entropy']
        self.entropy.columns = self.columns
        for c in np.arange(self.lcolumns):
            self.entropy.iloc[0, c] = 1 - self.k * self.dmatrix.iloc[:, c].sum()
        self.entropy.to_excel('entropy.xlsx')
    
    def getWeights(self):
        self.weights = pd.DataFrame(np.zeros((1, self.lcolumns)))
        self.weights.index = ['weights']
        self.weights.columns = self.columns
        for c in np.arange(self.lcolumns):
            self.weights.iloc[0, c] = self.entropy.iloc[0, c] / self.entropy.iloc[0, :].sum()
        print(self.weights)
        self.weights.to_excel('weights.xlsx')
