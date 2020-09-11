#-*-coding:utf-8-*-

from rtree import index
from Queue import PriorityQueue
import math
import KnnSearch as kn

MAX_DISTANCE = 286.7599520843743 
MAX_REV_COUNT = 7361
DtoR = 0.0174533 #Degree to Radian

def dist(plat, plon, lat, lon):
    delta = (plat-lat)**2 + (plon-lon)**2

    d = math.sqrt(delta)
    return d

class taalgorithm:
    
    def __init__(self, data,m):
        self.sorted_list= sorted(data, key = lambda x: x[1], reverse = True)
        self.knns = kn.knnsearch(data)
        self.fixed_m = m #m값 재귀함수에서 넘겨주기용    
            
    def topK(self, k, lat, lon, m, alpha_b, knnlist):
        #만일 top-k못찾으면 k 에 m*k 넣고 다시 실행
        #distance 수정
        print(k, m) 
        topklist = PriorityQueue(maxsize = k)
        knndict = dict()
        alpha = 1/(alpha_b+1)
        print('alpha:',alpha)
        
        for knn in knnlist:
            knndict[knn[0]]=knn[1:4]
            #knndict's element = (id : [review, katitude, longitude]) 
        i=0
        
        for key, value in knndict.items():
            distance = (MAX_DISTANCE - dist(value[1], value[2], lat, lon))/MAX_DISTANCE
            threshold = alpha*distance + (1-alpha)*(self.sorted_list[i][1]/MAX_REV_COUNT) #alpha*거리+(1-alpha)*평점
            Q = alpha*distance+(1-alpha)*(value[0]/MAX_REV_COUNT)
            
            
            if topklist.full():
                #mink는 score의 합과 id 둘다 갖는다.
                mink = topklist.get()
                if Q>mink[0]:
                    topklist.put((Q,key))
                else:
                    topklist.put(mink)                
            else:
                topklist.put((Q,key))
                
                
            Q = alpha*(MAX_DISTANCE-dist(self.sorted_list[i][2], self.sorted_list[i][3], lat, lon))/MAX_DISTANCE+ (1-alpha)*(self.sorted_list[i][1]/MAX_REV_COUNT)
            if topklist.full():
                mink = topklist.get()
                if Q>mink[0]:
                    topklist.put((Q,self.sorted_list[i][0]))
                else:
                    topklist.put(mink)
            else:
                topklist.put((Q,self.sorted_list[i][0]))
            i=i+1
            mink = topklist.get()
            if (mink[0] >= threshold):  #topklist의 최솟값이 threshold보다 크면
                topklist.put(mink)
                if(topklist.full()):
                    topklist_ = []
                    for j in range(k):
                        topklist_.insert(0, topklist.get())
                    #print(threshold)
                    return topklist_
                #else:
                    #print("NOT FULL",alpha,mink,threshold)
            else:   #topk list의 최솟값이 아직 threshold보다 작으면
                #print("mink still low")
                topklist.put(mink)
        
        virtual_k = len(knnlist)
        knnlist = self.knns.knn(self.sorted_list,lat,lon, int(round(m * virtual_k)))
        print(int(round(m * virtual_k)))
        topklist_ = self.topK(k, lat, lon, int(round(m*self.fixed_m)), alpha_b, knnlist)
        topklist_ = topklist_[0:k]
        return topklist_


if __name__ == '__main__':
    lat = input()
    lon = input()
    plat = input()
    plon = input()
