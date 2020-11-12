#-*-coding:utf-8-*-

from rtree import index
from Queue import PriorityQueue
import math
import pprint as p
import time
#import KnnSearch as kn

MAX_DISTANCE = 286.7599520843743 
MAX_REV_COUNT = 7361.0

def dist(plat, plon, lat, lon):
    delta = (plat-lat)**2 + (plon-lon)**2
    d = math.sqrt(delta)
    return d

file_name = "output_%f"%time.time()
#f = open(file_name,mode = 'wt')

class taalgorithm:
    
    def __init__(self, data,m,idx):
        self.sorted_list= sorted(data, key = lambda x: x[1], reverse = True)
        self.fixed_m = m #m값 재귀함수에서 넘겨주기용    
        self.idx = idx
        self.useless_time = 0 #time for knn
        self.lat = 0
        self.lon = 0
                    
    def topK(self, k, lat, lon, m, alpha_b, knnlist, option):
        #m은 안씀
        print(k,lat,lon)
        topklist_ = PriorityQueue(maxsize = k)
        #f.write(str(knnlist))
        self.lat = lat
        self.lon = lon
        if (option==0):
            alpha = 1/(1+alpha_b)
        else:
            alpha = alpha_b
        print alpha
        #flag, counter는 while loop 용
        flag = False
        counter = 0
        while flag == False:
            if(counter < 50):
                topklist_, flag = self.ThresholdAlgorithm(alpha, knnlist[counter],False, self.sorted_list[counter], topklist_)
                counter += 1
            else:
                topklist_, flag = self.ThresholdAlgorithm(alpha, knnlist[50-1], True, self.sorted_list[counter], topklist_)
                counter += 1
        
        final_topklist = list()
        for i in range(0,k):
            final_topklist.insert(0, topklist_.get())

        return final_topklist

    def ThresholdAlgorithm(self, alpha, knn_obj, last_knn_flag, poi_obj,topklist):
        if(poi_obj[2] == None and poi_obj[3] == None):
            return topklist, False
        topklist_list = list()
        topklist_list = topklist.queue
        knn_dist = dist(self.lat, self.lon, knn_obj[2], knn_obj[3])
        knn_dist = (MAX_DISTANCE - knn_dist)/MAX_DISTANCE
        poi_dist = dist(self.lat, self.lon, poi_obj[2], poi_obj[3])
        poi_dist = (MAX_DISTANCE - poi_dist)/MAX_DISTANCE
        poi_rev = poi_obj[1]/MAX_REV_COUNT
        knn_rev = knn_obj[1]/MAX_REV_COUNT
        #all of above normalized
        threshold = alpha*knn_dist+(1-alpha)*poi_rev #if mink is higher than threshold, set result_bool TRUE
        score_of_knn = alpha*knn_dist+(1-alpha)*knn_rev
        score_of_poi = alpha*poi_dist+(1-alpha)*poi_rev
        result_bool = False
        
        """
        f.write("\nt:")
        f.write(str(threshold))
        f.write(" knn: ")
        f.write(str(score_of_knn))
        f.write(" k.id rev dist:")
        f.write(str(knn_obj[0]))
        f.write(" ")
        f.write(str(knn_obj[1]))
        f.write(" ")
        f.write(str(knn_dist))
        f.write("|| poi: ")
        f.write(str(score_of_poi))
        f.write(" poi.id rev dist:")
        f.write(str(poi_obj[0]))
        f.write(" ")
        f.write(str(poi_obj[1]))
        f.write(" ")
        f.write(str(poi_dist))
        """

        #for knn
        if last_knn_flag == False:
            if (not topklist.full()) and not((score_of_knn, knn_obj[0]) in topklist_list):
                topklist.put((score_of_knn, knn_obj[0]))
            elif topklist.full() and not((score_of_knn, knn_obj[0]) in topklist_list):
                #f.write("\nqqq\n")
                min_k = topklist.get()
                if min_k[0] >= score_of_knn:
                    topklist.put(min_k)
                else:
                    topklist.put((score_of_knn, knn_obj[0]))
        #for poi
        if not topklist.full() and not((score_of_poi, poi_obj[0]) in topklist_list):
            topklist.put((score_of_poi, poi_obj[0]))
        elif topklist.full() and not((score_of_poi, poi_obj[0]) in topklist_list):
            #f.write("\n    aa    \n")
            min_k = topklist.get()
            if min_k[0] >= score_of_poi:
                topklist.put(min_k)
            else :
                topklist.put((score_of_poi, poi_obj[0]))

        #check threshold value
        if not topklist.full():
            result_bool = False
        else:
            min_k = topklist.get()
            if min_k[0] >= threshold:
                result_bool = True
            else:
                result_bool = False
            topklist.put(min_k)

        return topklist, result_bool

if __name__ == '__main__':
    lat = input()
    lon = input()
    plat = input()
    plon = input()
