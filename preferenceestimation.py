import math
class preferenceestimation:
    def __init__(self,n):
        self.sample_data = [] 
        self.sampleGeneration(n)
        self.preference = 0  
        
    # build sample data
    def sampleGeneration(self,n):
        # degree = 90 divided by (n+1) 
        degree = 90/float(n+1)
        for i in range(n):
           cur = degree*(i+1) # current_degree
           #print(cur)
           x = math.cos(math.radians(cur))
           y = math.sin(math.radians(cur))
           a = [i+1,round(x,2),round(y,2)]
           self.sample_data.append(a)
           i = i+1 # next point
        
    # estimate preference of the user

    # input : results = [[id, rank], [id,rank] ~~]
    # 1) compute the slope ( between 2 points )
    # 2) find out preferece possible region (Up/Down side of the slope)
    # 3) store the slope candidates and region data( 0 => upwards, 1 => downwards )
    # 4) find the largest value in upwards & smallest in downwards 
    # 5) average these 2 slope values => the final slop of the score function 
    
    def estimation(self,results,n):
        new_slope = [] # slope candidates
        p1 = [] # point 1 temp
        p2 = [] # point 2 temp
        
        for i in range(0,n):
            for j in range(i+1,n):
                p1 = self.sample_data[i]
                p2 = self.sample_data[j]

                # compute new slope
                # x value -> 1, y value -> 2
                x = p1[1]-p2[1]
                y = p1[2]-p2[2]
                slope = (float(x)/float(y))*(-1)
                slope = round(slope,2)
                # H = higher rank , L = lower rank
                # compare rank between 2 points
                
                if results[p1[0]] > results[p2[0]]:
                    # result[i] rank is lower than j
                    # store y value of each point
                    H = p2[2]
                    L = p1[2]
                else :
                    H = p1[2]
                    L = p2[2]
                

                # up side (1) vs. down side (0)
                temp = []
                if H > L:
                    # up side => [1, slope]
                    temp = [1,slope]
                else :
                    # down side => [0, slope]
                    temp = [0, slope]
                new_slope.append(temp)
        #print(new_slope,len(new_slope))
       
        # find largest & smallest value in slope candidate list
        largest = 0
        smallest = 100000 
        for i in range(0,len(new_slope)):
            if new_slope[i][0]==1:
                # upward => find max
                if new_slope[i][1] > largest:
                    largest = new_slope[i][1]
            else :
                # downward => find min
                if new_slope[i][1] < smallest:
                    smallest = new_slope[i][1]
        #self.preference = float(smallest+largest)/2 
        # tangent calculation 
        # smallest = tan a / largest = tan b
        # weight(score function) = tan ((a+b)/2)
       
        if largest == 0:
            #print('only minvalue')
            a = (-1 + math.sqrt(1+(smallest)*(smallest)))/(smallest)
            b = 0
        elif smallest == 100000:
            #print('only maxvalue')
            a = 1
            b = (-1 + math.sqrt(1+(largest)*(largest)))/(largest)
        else:
            a = (-1 + math.sqrt(1+(smallest)*(smallest)))/(smallest)
            b = (-1 + math.sqrt(1+(largest)*(largest)))/(largest)
        self.preference = (a+b)/(1-(a*b))
        self.preference = round(self.preference,3)
        #print(self.preference)
    
                

#dic = {1:3, 2:2, 3:1, 4:4}
#user = preferenceestimation(4)
#user.estimation(dic,4)
#print(user.sample_data)
#print(math.sin(math.radians(30)))

