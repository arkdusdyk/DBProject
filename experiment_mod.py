import csv
import UserInterface as UI
import accuracy
import GroundTruth
import json



class experiment():
    def __init__(self):
        print("experiment start")
        self.g_truth = []
        self.static = []
        self.dynamic = []
        self.ac = accuracy.accuracy()
        #self.topk = GroundTruth.GroundTruth()
        self.max_id = 100
    #def calculate_accuracy(self, ground_truth, target):

    def writeOutput(self,no):
        filename = 'mod_new_output_EX' + str(no) + '.csv'
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
        """
        with open("ground_truth.json") as gt_file:
            groundtruth = json.load(gt_file)
        with open("static.json") as s_file:
            static = json.load(s_file)
        with open("dynamic.json") as d_file:
            dynamic = json.load(d_file)
        """

        # header
        wr.writerow(['dataset_num','epoch_num' , 'method' , 'k', 'm', 'n', 'fagin','Query_Time'])
        # body
        if no == 1: # k experiment ( k = 1, 10, 20, 30, 40, 50 )
            print('k experiment start')
            for set_no in range(1,11):
                for epoch in range(1,11):                                                   # epoch 10
                    for k in (1,10,20,30,40,50):
                        jf1 = "[k]"+str(k)+'_try1_dataset'+str(set_no)+"new_ground_truth.json"
                        jf2 = "[k]"+str(k)+'_D'+str(set_no)+'T'+str(epoch)+"_dynamic.json"
                        jf3 = "[k]"+str(k)+'_D'+str(set_no)+'T'+str(epoch)+"_static.json"
                        print(jf2,jf3) 
                        with open(jf1) as gt_file:
                            groundtruth = json.load(gt_file)
                        with open(jf2) as d_file:
                            dynamic = json.load(d_file)
                        with open(jf3) as s_file:
                            static = json.load(s_file)
                    # initial condition
                    # accuracy
                        dynamic_fagin = 0     
                        static_fagin = 0
                    # process_time
                        dynamic_time = 0
                        static_time = 0
                    # loading .json data
                        for idx in range(0,100):                                              # user id = 100
                            ground = groundtruth[str(idx)]
                            dy_data = dynamic[str(idx)]
                            st_data = static[str(idx)]
                            dynamic_fagin += self.ac.Fagin(ground[0:k],dy_data[1:k+1])
                            static_fagin += self.ac.Fagin(ground[0:k],st_data[1:k+1])
                            dynamic_time += float(dy_data[0])
                            static_time += float(st_data[0])


                    # average of Fagin accuracy & processing time
                        dynamic_fagin /= self.max_id
                        static_fagin /= self.max_id
                        dynamic_time /= self.max_id
                        static_time /= self.max_id

                        print(dynamic_fagin, static_fagin, dynamic_time, static_time)

                    # dynamic 
                        wr.writerow([set_no,epoch, 1, k, static_m, static_n,dynamic_fagin,dynamic_time])
                    # static
                        wr.writerow([set_no,epoch, 2, k, static_m, static_n,static_fagin,static_time])
        elif no == 2: # m experiment
            print('m experiment start')
            for epoch in range(1,11):                                                   # epoch = 10
                for m in (1.5, 2, 2.5, 3, 3.5):
                    jf1 = "[m]"+str(m)+"_ground_truth.json"
                    jf2 = "[m]"+str(m)+"_dynamic.json"
                    jf3 = "[m]"+str(m)+"_static.json"
                    print(jf2,jf3) 
                    with open(jf1) as gt_file:
                        groundtruth = json.load(gt_file)
                    with open(jf2) as d_file:
                        dynamic = json.load(d_file)
                    with open(jf3) as s_file:
                        static = json.load(s_file)
                    # initial condition
                    # accuracy
                    dynamic_fagin = 0     
                    static_fagin = 0
                    # process_time
                    dynamic_time = 0
                    static_time = 0
                    # loading .json data
                    for idx in range(0,100):                                              # user id = 100
                        ground = groundtruth[str(idx)]
                        dy_data = dynamic[str(idx)]
                        st_data = static[str(idx)]
                        #print("{}:read {}th line".format(k,idx))  
                        dynamic_fagin += self.ac.Fagin(ground[0:static_k],dy_data[1:static_k+1])
                        static_fagin += self.ac.Fagin(ground[0:static_k],st_data[1:static_k+1])
                        dynamic_time += float(dy_data[0])
                        static_time += float(st_data[0])

                        #print(dynamic_fagin, static_fagin, dynamic_time, static_time)

                    # average of Fagin accuracy & processing time
                    dynamic_fagin /= self.max_id
                    static_fagin /= self.max_id
                    dynamic_time /= self.max_id
                    static_time /= self.max_id

                    # dynamic 
                    wr.writerow([epoch, 1, static_k, m, static_n,dynamic_fagin,dynamic_time])
                    # static
                    wr.writerow([epoch, 2, static_k, m, static_n,static_fagin,static_time])
        elif no == 3: # n experiment
            print('n experiment start')
            for set_no in range(1,11):
                for epoch in range(1,11):                                                   # epoch = 10
                    for n in (1, 3, 5, 7, 9):
                        jf1 = "[n]"+str(n)+'_try1_dataset'+str(set_no)+"new_ground_truth.json"
                        jf2 = "[n]"+str(n)+'_D'+str(set_no)+'T'+str(epoch)+"_dynamic.json"
                        jf3 = "[n]"+str(n)+'_D'+str(set_no)+'T'+str(epoch)+"_static.json"
                        print(jf2,jf3) 
                        with open(jf1) as gt_file:
                            groundtruth = json.load(gt_file)
                        with open(jf2) as d_file:
                            dynamic = json.load(d_file)
                        with open(jf3) as s_file:
                            static = json.load(s_file)
                    # initial condition
                    # accuracy
                        dynamic_fagin = 0     
                        static_fagin = 0
                    # process_time
                        dynamic_time = 0
                        static_time = 0
                    # loading .json data
                        for idx in range(0,100):                                              # user id = 100
                            ground = groundtruth[str(idx)]
                            dy_data = dynamic[str(idx)]
                            st_data = static[str(idx)]
                        #print("{}:read {}th line".format(k,idx))  
                            dynamic_fagin += self.ac.Fagin(ground[0:static_k],dy_data[1:static_k+1])
                            static_fagin += self.ac.Fagin(ground[0:static_k],st_data[1:static_k+1])
                            dynamic_time += float(dy_data[0])
                            static_time += float(st_data[0])

                        #print(dynamic_fagin, static_fagin, dynamic_time, static_time)

                    # average of Fagin accuracy & processing time
                        dynamic_fagin /= self.max_id
                        static_fagin /= self.max_id
                        dynamic_time /= self.max_id
                        static_time /= self.max_id
                    # dynamic 
                        wr.writerow([set_no, epoch, 1, static_k, static_m, n,dynamic_fagin,dynamic_time])
                    # static
                        wr.writerow([set_no, epoch, 2, static_k, static_m, n,static_fagin,static_time])
        f.close()
    '''
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
    '''
if __name__ == "__main__":
    ex = experiment()
    # k experiment.
    #ex.writeOutput(1)
    # n experiment
    ex.writeOutput(1)
    ex.writeOutput(3)
    """
    for i in range(1,4):
        ex.writeOutput(i) # intermediate files => 10 epochs
    """ 


