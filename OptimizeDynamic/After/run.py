from dynamic_update import dynamic_update
from random_cover import random_recover
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import linecache
from random import choice

class run:
    def read_file1(self):
        begin_line = 1    
        data_path = r'roads.txt' 
        all_all_sets = {}
        all_all_elements = {}
        with open("pathNums.txt", "r") as f1:
            for line in f1.readlines():
                line = line.strip('\n')  
                pathNum = int(re.findall(r"\d+",line)[0])
                once_dict = {}
                elements = set()
                j = 0
                for i in range(begin_line, begin_line + pathNum):
                    content = linecache.getline(data_path, i).strip('\n')
                    point = re.findall(r"\d+",content)
                    point_int = set()
                    for e in point:
                        point_int.add(int(e))
                        elements.add(int(e))
                    once_dict[j] = point_int
                    j+=1
                begin_line = begin_line + pathNum
                all_all_sets[pathNum] = once_dict
                all_all_elements[pathNum] = elements
        return all_all_sets,all_all_elements                   
    
    def input_all(self,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p):
        # Initialize all elements need to be cover
        self.all_elements = set()
        self.S = {}   
        self.sets_len = len(self.S)
        # solution F
        self.F = {}
        # PDU
        self.P = P
        self.D = D
        self.U = U
        self.Pi = Pi
        self.Di = Di
        self.Ui = Ui
        self.All_p = All_p
        self.S_p = S_p
        self.X_p = X_p
        self.Orig_p = Orig_p
        self.Extra_p = Extra_p
        self.param_l = 0.4
        self.A= set()
    
    def do_adding_and_removing(self, add_elements, remove_elements, last_result):
        DU = dynamic_update(
                            self.param_l,
                            self.all_elements, self.S, add_elements, remove_elements, last_result, 
                            self.All_p, self.S_p, self.X_p, self.Orig_p, self.Extra_p, 
                            self.P, self.D, self.U,
                            self.Pi, self.Di, self.Ui,self.A
                            )
        
        result_added,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p,self.A = DU.add_deal()
        DU.remove_deal()        
        self.F = DU.get_F()
        result_removed = self.F
        return result_added, result_removed,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p,self.Orig_p,self.Extra_p,self.A

    def run_main(self, add_elements, remove_elements, all_sets, all_elements, last_result,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A):
        self.input_all(P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p)
        self.A = A
        self.S = all_sets
        lenth = len(all_sets)
        self.all_elements = all_elements
        start = time.time()
        result_added, result_removed,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A = self.do_adding_and_removing(add_elements, remove_elements, last_result)
        end = time.time()
        timeneed = end-start
        cpu = 0
        for key,value in result_added.items():
            cpu = cpu + len(value)
        return timeneed, lenth, len(result_removed), cpu, result_removed,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A
    
    def get_points(self):
        begin_line = 1    
        data_path = r'points0.2.txt' 
        all_points = {}
        for i in range(23):
            content = linecache.getline(data_path, i+1).strip('\n')
            point = re.findall(r"\d+",content)
            point_int = set()
            for e in point:
                point_int.add(int(e))
            all_points[i] = point_int
            begin_line+=1
        return all_points        
        
RUN = run()
abnormal = 0.2 # abnormal rate
all_all_sets1,all_all_elements1= RUN.read_file1()
all_all_points = RUN.get_points()
path_array1 = []
for key in all_all_sets1.keys():
    if key!=1:
        path_array1.append(key)
time_array = []
totalcpu_array = []
cpu_array = []
path_array = []
for i in range(0,7):
    for key,value in all_all_sets1.items():
        if key == path_array1[i]:
            S = value
            E = all_all_elements1.get(key)
    AE = E  
    all_points = all_all_points.get(i)
    total_cpu=0
    for u in range(len(S)):
        total_cpu = total_cpu +len(S.get(u))          
    results = {}
    result = {}
    all_sets = S.copy()
    all_elements = E.copy()
    add_elements = all_points.copy()
    cpu_sum = 0
    time_sum = 0
    start = time.perf_counter()
    for j in range(100):    
        result = {}
        F = {}
        P = {}
        D = set()
        U = set()
        Pi = {} 
        Di = {}
        Ui = {}
        for i in range(100):
            Pi[i] = set()
            Di[i] = set()
            Ui[i] = set()
        All_p = set()
        S_p = {}
        X_p = {}
        Orig_p = {}
        Extra_p = {}
        A = set()
        remove_elements = set()
        last_result = {}
        timeneed, lenth, covered_len, c, result,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A = RUN.run_main(add_elements.copy(), remove_elements.copy(),all_sets.copy(), all_elements.copy(), last_result.copy(),P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A)
        cpu = c*15+(total_cpu-c)*10
        cpu_sum = cpu + cpu_sum
    end = time.perf_counter()
    timeneed = end - start
    timeneed_av = timeneed/100
    cpu_av = cpu_sum//100
    formated_time = '{:.15f}'.format(timeneed_av)
    print("time: ", formated_time)
    time_array.append(formated_time)
    print("cpu: ", cpu_av)
    cpu_array.append(cpu_av)
    print("total cpu: ",total_cpu*15)
    totalcpu_array.append(total_cpu)
    print("total paths: ", len(S), " ",covered_len)
    path_array.append(len(S))
    
with open("data.txt","a") as ff:
    for e in time_array:
        ff.write(e+" ")
    ff.write("\n") 
    for e in cpu_array:
        ff.write(str(e)+" ")
    ff.write("\n") 
    for e in totalcpu_array:
        ff.write(str(e*15)+" ")
    ff.write("\n") 
    for e in path_array:
        ff.write(str(e)+" ")      
