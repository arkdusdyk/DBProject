#-*- coding: utf-8 -*-
import json


class UserInterface():
	def __init__(self, m, n):
		self.data = []
		self.results = {}	#dictionary = {data: 순위}
		self.m = m
		self.n = n			#preference estimation sample data 갯수
		self.inputUser()
		self.readdata(filename)
		self.PE = preferenceestimation(self.n)

		#review count sorted list

		#samplegeneration(self, self.n)

	def readData(self, filename):
	#extract json file -> data list 에 [id, review, lat, long] 형식으로 저장
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
		#json line 읽으면서 parsing

	def inputUser(self):
	#user input (initial)
		self.username = input('Name: ')
		self.lon = input('Location Longitude: ')
		self.lat = input('Location Latitude: ')
		self.k = input('Top-K: ')

	def outputuser(self, topklist):

		#return top-k result

	def doTopK(self):
		return topk(self.k, self.lat, self.lon, self.m, self.a, self.knn)

	#def interaction(self):
		#preferenceestimation(self.data)


if __name__ == "__main__":
	filename = "business.json"
	ui = UserInterface(2,3)			#m,n값 실험하면서 변화
	topkresult = ui.dotopk()		#topklist returned
	ui.outputuser(topkresult)
	
