#-*- coding: utf-8 -*-
import json
import preferenceestimation as pe
import KnnSearch as knns

class UserInterface():
    def __init__(self, m, n):
        self.data = []
        self.results = {}
        self.m = m
        self.n = n                  #preference estimation sample data
        self.poi = []                   #review count sorted list
        self.readData(filename)
        self.knn = knns.knnsearch(self.data)        #knnsearch init, r-tree index
        self.inputUser()
        self.pepe = pe.preferenceestimation(self.n)    #sample generation
        self.sd = self.pepe.sample_data
	

    def readData(self, filename):
    #extract json file -> data list 에 [id, review, lat, long] 형식으로 저장 + poi 정렬해서 attribute로 저장
        initlist = []
        for line in open(filename,'r'):
            initlist.append(json.loads(line))
        i=0
        for line in initlist:
            extract = []
            extract.append(i)
            extract.append(line['review_count'])
            extract.append(line['latitude'])
            extract.append(line['longitude'])
            self.data.append(extract)
            i = i+1
        #self.data : 2D list of [id, review, lat, long]
        self.poi = sorted(initlist, key = lambda k: k['review_count'], reverse = True)


    def inputUser(self):
    #user input (initial)
        self.username = input('Name: ')
        self.user_lon = input('Location Longitude: ')
        self.user_lat = input('Location Latitude: ')
        self.k = input('Top-K: ')
    
    def doKNN(self):
        self.knnlist = self.knn.knn(self.data, self.user_lat, self.user_lon, self.k)
        print(self.knnlist)
    
    #def outputuser(self, topklist):
        #return top-k result

    #def doTopK(self):
        #self.topklist

    def interaction(self):
        rank = []
        print('Sample Locations: ')
        for i in self.sd:
            print(i)
        print('Start Ranking in order: ')
        rank = list(map(int, input().split()))
        idx = 0
        for i in self.sd:
            self.results[i[0]] = rank[idx]
            idx = idx+1
        print(self.results)
        self.pepe.estimation(self.results, self.n)
        self.a = self.pepe.preference
        print(self.a)


if __name__ == "__main__":
    filename = "business.json"
    ui = UserInterface(2,3)	    #m,n값 실험하면서 변화
    ui.interaction()
    #ui.doTopK()        #topklist returned
    #ui.outputuser(topkresult)
	
