import math
from itertools import combinations
from scipy import stats
# top-k list accuracy

class accuracy:

    def __init__(self):
        self.intersection = []
        self.F_accuracy = 0
        self.K_accuracy = 0
        
    # Fagin equation - "rank"
    def Fagin(self, correct_answer, result):
        # find intersection 
        self.intersection=[]
        length = len(correct_answer)
    
        for i in range(0,length):
            for j in range(0,length):
                # if ID is same 
                if correct_answer[i][1] == result[j][1]:
                    self.intersection.append((i+1,j+1))
                #j = j+1
            #i = i+1
        # length of intersection 
        len_of_inter= len(self.intersection)
        combi=list(combinations(self.intersection,2))
        #print(self.intersection)
        #print(combi)
        #print(len_of_inter)
        sum_of_i = 0    # sum of pie ranks
        sum_of_j = 0    # sum of pie' ranks
        sum_of_dif = 0  # sum of difference between pie & pie'
        SUM = (length*(length+1))
        for k in range(0,len_of_inter):
            # [0] => i / [1] => j
            sum_of_i = sum_of_i + self.intersection[k][0]
            sum_of_j = sum_of_j + self.intersection[k][1]
            left = combi[k][0]    
            right = combi[k][1]
            #print(left,right)
            #print(left[0],right[0], left[1],right[1])
            
            dif = (left[0]-right[0])*(left[1]-right[1])
            
            if dif < 0:
               sum_of_dif += 1
        #print(sum_of_dif,length,len_of_inter,sum_of_i,sum_of_j, SUM) 
        #print(self.intersection) 
        F = sum_of_dif + 2*(length-len_of_inter)*(length+1) + sum_of_i + sum_of_j - SUM
        self.F_accuracy =( 1 - float(F)/float(SUM))
        
        return round(self.F_accuracy,3)
        
    # Kendall Tau - "order"
    def kendalltau(self,correct_answer,result):
        length = len(correct_answer)
        # scipy -> tau-b version 
        x = []; y=[]
        for i in range(0,length):
            x.append(correct_answer[i][1])
            #i += 1
        for j in range(0,length):
            y.append(result[j][1])
            #j += 1
        
        print(x)
        print(y)
        tau, p_value = stats.kendalltau(x, y)
        #print(tau)
        #print(p_value)
        # -1 <= tau <=1 
        self.K_accuracy = tau
        print('Kendall Rank correlation %.5f' % tau)
        #print(p_value)
        return round(self.K_accuracy,3)

