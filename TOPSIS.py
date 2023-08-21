import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',None)

#Different types of indicators are positively oriented in different ways.
#This requires you to define one or more simple functions to positively orient one or more indicators.
#Of course, this needs to be done in advance.

class Topsis:
    
    def __init__(self, info):
        self.info = info
        self.index = info.index
        self.columns = info.columns
        self.lrows = len(info.index)
        self.lcolumns = len(info.columns)
    
    def Forwardization(self):
        pass
    
    def Normalization(self):
        self.ndata = pd.DataFrame(np.zeros((self.lrows, self.lcolumns)))
        self.ndata.index = self.index
        self.ndata.columns = self.columns
        for c in np.arange(self.lcolumns):
            for r in np.arange(self.lrows):
                self.ndata.iloc[r, c] = (self.info.iloc[r, c] - self.info.iloc[:, c].min()) / (self.info.iloc[:, c].max() - self.info.iloc[:, c].min())
                
        
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
        self.ndata.to_excel('ndata_topsis_xij.xlsx'); self.sndata.to_excel('sndata_topsis_xij.xlsx')
            
    def getZmm(self):
        self.zmm = pd.DataFrame(np.zeros((2, self.lcolumns)))
        self.zmm.columns = self.columns
        self.zmm.index = ["Z+", "Z-"]
        for c in np.arange(self.lcolumns):
            self.zmm.iloc[0, c] = self.ndata.iloc[:, c].max()
            self.zmm.iloc[1, c] = self.ndata.iloc[:, c].min()
        self.zmm.to_excel('zmm.xlsx')
        
    def getDmm(self, weights):
        self.weights = weights
        self.dmm = pd.DataFrame(np.zeros((self.lrows, 2)))
        self.dmm.columns = ["D+", "D-"]
        self.dmm.index = self.index
        Dmax = 0; Dmin = 0
        for r in np.arange(self.lrows):
            Dmax = 0; Dmin = 0
            for c in np.arange(self.lcolumns):
                Dmax += self.weights.iloc[0, c]*(self.zmm.iloc[0, c] - self.ndata.iloc[r, c])**2
                Dmin += self.weights.iloc[0, c]*(self.zmm.iloc[1, c] - self.ndata.iloc[r, c])**2
            self.dmm.iloc[r, 0] = np.sqrt(Dmax)
            self.dmm.iloc[r, 1] = np.sqrt(Dmin)
        self.dmm.to_excel('dmm.xlsx')
        
    def getScores(self):
        self.sscore = pd.DataFrame(np.zeros((self.lrows, 1)))
        self.score = self.sscore
        self.score.index = self.index
        self.score.columns = ['score']
        for r in np.arange(self.lrows):
            self.sscore.iloc[r, 0] = self.dmm.iloc[r, 1] / (self.dmm.iloc[r, 0] + self.dmm.iloc[r, 1])
        for rs in np.arange(self.lrows):
            self.score.iloc[rs, 0] = self.sscore.iloc[rs, 0] / self.sscore.iloc[:, 0].sum()
        print(self.score.sort_values(by = 'score', ascending = False))
        self.score.sort_values(by = 'score', ascending = False).to_excel('score.xlsx')
