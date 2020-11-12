#-*coding:utf-8-*-
from rtree import index

class knnsearch:
    
    def __init__(self,data):
        self.index = index.Index()
        self.rtree(data)
            
    def knn(self, data, currentlat, currentlon, k):
        knnlist = []
        knn_id_list = list(self.index.nearest((currentlat, currentlon, currentlat, currentlon),50))#return only id
        knn_id_list = map(int,knn_id_list)
        #print(knn_id_list)
        data_dic = dict()
        #for searching by id, make dictionary
        for items in data:
            idfordata = '%d'%items[0]
            data_dic[idfordata]=items[1:4]
        for idx in knn_id_list:
            idx_str = '%d'%idx
            tmp = []
            tmp = [idx]
            tmp.extend(data_dic[idx_str])
            #tmp = [id, review, lat, lon] by knn
            knnlist.append(tmp)
        #print(knnlist)
        return knnlist

    def rtree(self, data):
        for ones in data:
            #print(ones[0])
            if (ones[2] == None or ones[3] == None):
                continue
            self.index.insert(ones[0],(ones[2],ones[3],ones[2],ones[3]))
