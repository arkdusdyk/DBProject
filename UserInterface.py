#-*- coding: utf-8 -*-
import json
import preferenceestimation as pe
import KnnSearch as knns
import TopkSearch as topkk

class UserInterface():
    def __init__(self, m, n):
        self.data = []
        self.results = {}
        self.m = m
        self.n = n                  #preference estimation sample data
        self.poi = []                   #review count sorted list
        print("Reading Data...")
        self.readData(filename)
        print("Reading, sorting POI done...")
        print("Initial Rtree Indexing...")
        self.knn = knns.knnsearch(self.data)        #knnsearch init, r-tree index
        print("Rtree Indexing Done")
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
        self.user_lon = input('Location Longitude: ')
        self.user_lat = input('Location Latitude: ')
        self.k = input('Top-K: ')
    
    def doKNN(self):
        self.knnlist = self.knn.knn(self.data, self.user_lat, self.user_lon, self.k)
    
    def outputuser(self):
        print(self.topklist)

    def doTopK(self):
        print('Initialize TA-Algorithm')
        self.topk = topkk.taalgorithm(self.data)
        print('Processing TA Algorithm')
        self.topklist = self.topk.topK(self.k, self.user_lat, self.user_lon, self.m, self.a, self.knnlist)
        print('Top-k Done')

    def interaction(self):
        rank = []
        print('Sample Locations: ')
        for i in self.sd:
            print(i)
        print('Start Ranking in order: ')
        #rank = list(map(int, input().split()))
        rank_str = raw_input()
        rank_list = rank_str.split()
        map_object = map(int, rank_list)
        rank = list(map_object)
        idx = 0
        for i in self.sd:
            self.results[i[0]] = rank[idx]
            idx = idx+1
        self.pepe.estimation(self.results, self.n)
        self.a = self.pepe.preference
        print 'User Preference : {}'.format(self.a)


if __name__ == "__main__":
    filename = "business.json"
    ui = UserInterface(2,3)	    #m,n값 실험하면서 변화
    ui.interaction()
    ui.doKNN()
    ui.doTopK()                 #topklist returned
    ui.outputuser()
