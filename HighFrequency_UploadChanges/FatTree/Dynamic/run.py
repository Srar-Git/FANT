from dynamic_update import dynamic_update
from random_cover import random_recover
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import linecache
from random import choice

class run:
    def read_file(self):
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
                    once_dict["path"+str(j)] = point_int
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
                              
    def get_gap(self,result1, result2):
        jiao = result1.keys() & result2.keys()
        cha1 = result1.keys() - jiao
        cha2 = result2.keys() - jiao
        lenth = 0
        paths=0
        if cha1:
            for e in cha1:
                paths+=1
                lenth = lenth + len(S.get(e))
        if cha2:
            for e in cha2:
                paths+=1
                lenth = lenth + len(S.get(e))
        return lenth,paths 
        
RUN = run()
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
all_all_sets,all_all_elements = RUN.read_file()
for key,value in all_all_sets.items():
    if key == 90:
        S = value
        E = all_all_elements.get(key)
total_cpu1=0
for u in range(len(S)):
    total_cpu1 = total_cpu1 +len(S.get("path"+str(u)))     
all_points = RUN.get_points()
results = {}
result = {}
data = "date.txt"
total_time=0
total_diff=0
total_l=0
total_cpu=0
for i in range(100):
    all_sets = S.copy()
    all_elements = E.copy()
    
    add_elements = all_points.get(i)
    if i-1 < 0:
        remove_elements = set()
    else:
        remove_elements = all_points.get(i-1)- all_points.get(i)
    if i-1 < 0:
        last_result = {}
    else:
        last_result = results.get(i-1)
    last_result2 = last_result.copy()
    timeneed, lenth, covered_len, c, result,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A = RUN.run_main(add_elements, remove_elements,all_sets, all_elements, last_result,P,D,U,Pi,Di,Ui,X_p,S_p,All_p,Orig_p,Extra_p,A)
    total_time+=timeneed
    cpu = c*15+(total_cpu1-c)*10
    results[i] = result
    
    result2 = results.get(i)
    l,p = RUN.get_gap(last_result2, result2)
    total_diff+=l
    total_l+=p
    total_cpu+=cpu
    print("difference：",l,"(",p,"roads)",data)
    print("cpu_total: ", total_cpu1*15,data)
    print("=====================timepoint: ",i,"====================",data)
p_time= total_time/100
p_diff=total_diff/100
p_l = total_l/100
p_cpu = total_cpu/100
print("time: ",p_time)    
print("difference: ",p_diff)    
print("roads: ",p_l) 
print("cpu: ",p_cpu) 