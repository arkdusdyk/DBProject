import csv
import UserInterface as UI
import accuracy
import GroundTruth

class experiment():
    def __init__(self):
        print("experiment start")
        self.g_truth = []
        self.static = []
        self.dynamic = []
        self.ac = accuracy.accuracy()
        self.topk = GroundTruth.GroundTruth()

    #def calculate_accuracy(self, ground_truth, target):

    def writeOutput(self,no):
        filename = 'output_EX' + str(no) + '.csv'
        print(filename)
        f = open(filename,'w')
        wr = csv.writer(f)

        # default parameters (base lines...?)
        static_k = 30
        static_m = 2.5
        static_n = 5

        # accuracy calculation - only "Fagin"
        """
        g_truth = [(1,123), (2,32), (3,4534)]
        static = [(3,32),(5, 4534),(2,123)]
        dynamic = [(3,123), (8,4534),(3,32)]
        self.fagin_s = self.ac.Fagin(g_truth,static)
        #self.kendall_s = self.ac.kendalltau(g_truth,static)
        print('static')
        print(self.fagin_s)
        self.fagin_d = self.ac.Fagin(g_truth,dynamic)
        #self.kendall_d = self.ac.kendalltau(g_truth,dynamic)
        print('dynamic')
        print(self.fagin_d)
        """
        
        # header
        wr.writerow(['epoch_num' , 'method' , 'k', 'm', 'n', 'fagin','Query_Time'])
        # body
        if no == 1: # k experiment ( k = 1, 10, 20, 30, 40, 50 )
            print('k experiment start')
            for epoch in range(1,11):
                for k in (1,10,20,30,40,50):
                    # dynamic 
                    wr.writerow([epoch, 1, k, static_m, static_n,'fagin','query_time'])
                    # static
                    wr.writerow([epoch, 2, k, static_m, static_n,'fagin','query_time'])
        elif no == 2:
            print('m experiment start')
            for epoch in range(1,11):
                for m in (1.5, 2, 2.5, 3, 3.5):
                    # dynamic 
                    wr.writerow([epoch, 1, static_k, m, static_n,'fagin','query_time'])
                    # static
                    wr.writerow([epoch, 2, static_k, m, static_n,'fagin','query_time'])
        elif no == 3:
            print('n experiment start')
            for epoch in range(1,11):
                for n in (1, 3, 5, 7, 9):
                    # dynamic 
                    wr.writerow([epoch, 1, static_k, static_m, n,'fagin','query_time'])
                    # static
                    wr.writerow([epoch, 2, static_k, static_m, n,'fagin','query_time'])
        f.close()
    def writeFinal(self,no): 
        # write final file
        filename = 'final_EX' + str(no) + '.csv'
        print(filename)
        f = open(filename,'w')
        wr = csv.writer(f)
        
        # read intermediate file
        filename2 = 'output_EX' + str(no) + '.csv'
        fp = open(filename,'r')
        rd = csv.reader(fp)

        # average
        average = 0

        # header
        wr.writerow(['epoch_num' , 'method' , 'k', 'm', 'n', 'fagin','Query_Time'])
        # body
        if no == 1:
            print('k final report')
            #for row in reader:
        elif no == 2:
            print('m final report')
        elif no == 3:
            print('n final report')
        f.close()
if __name__ == "__main__":
    ex = experiment()
    for i in range(1,4):
        ex.writeOutput(i) # intermediate files => 10 epochs
        #ex.writeFinal(i) # final files => Averages
        


