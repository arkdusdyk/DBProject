#-*-coding:utf-8-*-

from rtree import index
from Queue import PriorityQueue
import math

MAX_DISTANCE = 180*0.0174533*6371 #sqrt(360^2 + 180^2)
MAX_REV_COUNT = 7361
DtoR = 0.0174533 #Degree to Radian

def dist(plat, plon, lat, lon):
    deltalat = DtoR*abs(plat - lat)
    deltalon = DtoR*abs(plon-lon)
    temp = math.sin(deltalat/2)**2 + math.cos(DtoR*plat)*math.cos(DtoR*lat)*(math.sin(deltalon/2)**2)
    delta = 2*math.asin(math.sqrt(temp))
    d = delta*6371 #6371 = earth's diameter
    return d

class taalgorithm:
    
    def __init__(self, data):
        self.sorted_list= sorted(data, key = lambda x: x[1], reverse = True)

    def topK(self, k, lat, lon,m,alpha, knnlist):
        #만일 top-k못찾으면 k 에 m*k 넣고 다시 실행
        #distance 수정 필요
        topklist = PriorityQueue( maxsize = k )
        knndict = dict()
        for knn in knnlist:
            knndict[knn[0]]=knn[1:4]
            #knndict's element = (id : [review, katitude, longitude]) 
        i=0
        for key, value in knndict.items():
            distance = (MAX_DISTANCE - dist(value[1], value[2], lat, lon))/MAX_DISTANCE
            threshold = alpha*distance + (1-alpha)*(self.sorted_list[i][1]/MAX_REV_COUNT) #alpha*거리+(1-alpha)*평점
            Q = alpha*distance+(1-alpha)*(value[0]/MAX_REV_COUNT)
            if topklist.full():
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
                    topklist.put((Q,sorted_list[i][0]))
                else:
                    topklist.put(mink)
            else:
                topklist.put((Q,sorted_list[i][0]))
            i=i+1
            if (mink > threshold and topklist.full()):
                topklist_ = []
                for j in range(k):
                    topklist_.insert(0, topklist.get())
                return topklist_
        if not topklist.full():
            topklist_ = self.ta(knnlist, alpha, lat, lon, k*m, m)
            return topklist_


if __name__ == '__main__':
    lat = input()
    lon = input()
    plat = input()
    plon = input()
    print(dist(plat,plon,lat,lon))
