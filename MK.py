import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MK:
    
    def __init__(self, data, num):
        self.data = data
        self.data1 = np.array(data)
        self.data2 = self.data1[::-1]
        self.n = num
        self.Ufk = np.zeros(num)
        self.Ubks = np.zeros(num)
        self.Ubk = np.zeros(num)
        
    @property    
    def Kendall_change_point_detection(self):
        Sk1 = np.zeros(self.n); Sk2 = np.zeros(self.n)
        s1 = 0; s2 = 0
        E1 = np.zeros(self.n); E2 = np.zeros(self.n)
        Var1 = np.zeros(self.n); Var2 = np.zeros(self.n)
        
        for i in range(1,self.n):
            for j in range(i):
                if self.data1[i] > self.data1[j]:
                    s1 += 1
                else:
                    pass
            Sk1[i] = s1
            E1[i] = (i + 1)*(i + 2)/4                      
            Var1[i] = (i + 1)*i*(2*(i + 1) + 5)/72             
            self.Ufk[i] = (Sk1[i] - E1[i])/np.sqrt(Var1[i])
            
        for i in range(1,self.n):
            for j in range(i):
                if self.data2[i] > self.data2[j]:
                    s2 += 1
                else:
                    pass
            Sk2[i] = s2
            E2[i] = (i+1)*(i+2)/4                      
            Var2[i] = (i+1)*i*(2*(i+1)+5)/72             
            self.Ubks[i] = (Sk2[i] - E2[i])/np.sqrt(Var2[i])
            self.Ubk[i] = -self.Ubks[i]
        self.Ubk = self.Ubk[::-1] 

        diff = np.array(self.Ufk) - np.array(self.Ubk)
        K = []

        for k in range(1,self.n):
            if diff[k - 1]*diff[k]<0:
                K.append(k)
 
        plt.figure(figsize=(12,8))
        plt.plot(self.data.index ,self.Ufk  ,label='UFK') 
        plt.plot(self.data.index ,self.Ubk ,label='UBK') 
        plt.ylabel('UFK-UBK')
        x_lim = plt.xlim()
        plt.plot(x_lim,[-1.96,-1.96],'m--',color='r')
        plt.plot(x_lim,[  0  ,  0  ],'m--')
        plt.plot(x_lim,[+1.96,+1.96],'m--',color='r')
        plt.grid()
        plt.legend() 
        plt.show()
        return K
