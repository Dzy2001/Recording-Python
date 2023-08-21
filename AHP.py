import numpy as np

#Indicator weights can be obtained by arithmetic mean, geometric mean, and vector eigenvalue methods.
#To ensure that the conclusions reached by the AHP method are reasonable, the judgment matrix of the AHP method must be consistent.
#Default passes the test when CR is less than 0.1.

class AHP:

    def __init__(self, array):
        self.array = array
        self.n = array.shape[0]
        self.RI_list = [0, 0, 0.52, 0.89, 1.12, 1.26, 
                        1.36, 1.41, 1.46, 1.49, 1.52, 
                        1.54, 1.56, 1.58, 1.59]
        self.eig_val, self.eig_vector = np.linalg.eig(self.array)
        self.max_eig_val = np.max(self.eig_val)
        self.max_eig_vector = self.eig_vector[:, np.argmax(self.eig_val)].real
        self.CI_val = (self.max_eig_val - self.n) / (self.n - 1)
        self.CR_val = self.CI_val / (self.RI_list[self.n - 1])

    def test_consist(self):
        print("CI：" + str(self.CI_val))
        print("CR：" + str(self.CR_val))
        if self.n == 2:  
            print("Contains only two subfactors, no consistency issues.")
        else:
            if self.CR_val < 0.1: 
                print("CR: " + str(self.CR_val) + "Pass consistency check!")
                return True
            else: 
                print("CR: " + str(self.CR_val) + "Failed consistency check!")
                return False

    def cal_weight_by_arithmetic_method(self):
        col_sum = np.sum(self.array, axis=0)
        array_normed = self.array / col_sum
        array_weight = np.sum(array_normed, axis=1) / self.n
        print("The weight vector calculated by the arithmetic mean method is：\n", 
              array_weight)
        return array_weight

    def cal_weight__by_geometric_method(self):
        col_product = np.product(self.array, axis=0)
        array_power = np.power(col_product, 1 / self.n)
        array_weight = array_power / np.sum(array_power)
        print("The weight vector calculated by the geometric mean method is：\n", 
              array_weight)
        return array_weight

    def cal_weight__by_eigenvalue_method(self):
        array_weight = self.max_eig_vector / np.sum(self.max_eig_vector)
        print("The weight vector calculated by the eigenvalue method is：\n", 
              array_weight)
        return array_weight
