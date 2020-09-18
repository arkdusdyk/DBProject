#-*- coding: utf-8 -*-
import json
import KnnSearch as knns
import TopkSearch as topkk
import time

class GroundTruth():
    def __init__(self, m, n):
        self.m = m
        self.n = n                  #preference estimation sample data
        self.k = 50
        self.option=1
        self.mode =2                #mode : 0 (ground_truth), 1 (dynamic), 2 (0.5 static)
        print("Reading Data...")
        initlist = []
        for line in open("business.json",'r'):
            initlist.append(json.loads(line))
        i=0
        self.data = []
        for line in initlist:
            extract = []
            extract.append(i)
            extract.append(line['review_count'])
            extract.append(line['latitude'])
            extract.append(line['longitude'])
            self.data.append(extract)
            i=i+1
        #self.data : 2D list of [id,review, lat, lon]
        self.poi = sorted(initlist, key = lambda k: k['review_count'], reverse = True)
        print("Reading, sorting POI done...")
        print("Initial Rtree Indexing...")
        self.knn = knns.knnsearch(self.data)        #knnsearch init, r-tree index
        print("Rtree Indexing Done")
        self.trueData(filename, self.mode)

    def trueData(self, filename, mode):
    #extract json file -> datalist
        with open(filename) as json_file:
            json_data = json.load(json_file)
        json_file.close()
        true_data = dict()
        for i in range(0,100):    
            user = json_data[str(i)]
            self.user_id = user["id"]
            self.user_lat = user["lat"]
            self.user_lon = user["lon"] 
            self.knnlist = self.knn.knn(self.data, self.user_lat, self.user_lon, self.k)
            print('Initialize TA-Algorithm')
            self.topk = topkk.taalgorithm(self.data, self.m, self.knn.index)
            if mode==2 :        #static (0.5 fixed)
                self.user_alpha = 0.5
            else :              #ground_truth or dynamic (user defined)
                self.user_alpha = user["alpha"]
            print('Processing TA Algorithm')
            self.topklist = self.topk.topK(self.k, self.user_lat, self.user_lon, self.m, self.user_alpha, self.knnlist,self.option)
            print('Top-k Done')
            j=1
            temp_list = list()
            for lists in self.topklist:
                topkdict = dict()
                topkdict[j] = self.topklist[j-1]
                temp_list.append(topkdict[j])
                j=j+1
            true_data[self.user_id] = temp_list
            if self.mode==0:
                with open('ground_truth.json','w') as outfile:
                    json.dump(true_data,outfile,indent=4)
            else:   #static
                with open('static.json','w') as outfile:
                    json.dump(true_data,outfile, indent=4)
            '''elif self.mode==1:
                with open('dynamic.json','w') as outfile:
                    json.dump(true_data,outfile, indent=4)
            '''

if __name__ == "__main__":
    filename = "dataset.json"
    gt = GroundTruth(2.5,5)
