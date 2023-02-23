import re
import time
from random import choice
import linecache
from timeit import default_timer as timer

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
                    once_dict[j] = point_int
                    j+=1
                begin_line = begin_line + pathNum
                all_all_sets[pathNum] = once_dict
                all_all_elements[pathNum] = elements
        return all_all_sets,all_all_elements            
    def main(self, all_elements, all_sets):
        lenth = len(all_sets)
        final_all_sets = set()
        i = 1
        while all_elements:
            best_station = None
            states_covered = set()
            for station, states in all_sets.items():
                covered = all_elements & states
                covered_cost = len(covered)/len(states)
                if covered_cost > len(states_covered)/len(states):
                    best_station = station
                    states_covered = covered
            all_elements -= states_covered
            final_all_sets.add(best_station)
            i += i
        covered_len = len(final_all_sets)
        cpu = 0
        result_sets = {}
        for path in final_all_sets:
            cpu = cpu + len(all_sets.get(path))
            result_sets[path] = all_sets.get(path)
        return result_sets,lenth, covered_len, cpu
    def save_points(self,all_elements,n, times,filename):
        for i in range(times):
            for i in range(n):
                e = str(choice(list(all_elements)))
                with open(filename,"a") as ff:
                    ff.write(e+" ")   
            with open(filename,"a") as f2:   
                f2.write("\n") 
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
abnormal = 0.3 #the abnormal rate
all_all_sets,all_all_elements= RUN.read_file()
path_array1 = []
for key in all_all_sets.keys():
    if key!=1:
        path_array1.append(key)
all_all_points = RUN.get_points()
time_array = []
totalcpu_array = []
cpu_array = []
path_array = []
print("total times: ", len(path_array1))
for i in range(0,len(path_array1)):
    S = all_all_sets.get(i)
    AE = all_all_elements.get(path_array1[i])
    # run this to get the abnormal points
    # RUN.save_points(AE.copy(),round(len(AE)*abnormal),1 , "points0.2.txt")
    for key,value in all_all_sets.items():
        if key == path_array1[i]:
            S = value
    all_points = all_all_points.get(i)
    total_cpu=0
    for u in range(len(S)):
        total_cpu = total_cpu +len(S.get(u))          
    results = {}
    result = {}
    all_sets = S.copy()
    add_elements = all_points.copy()
    cpu_sum = 0
    time_sum = 0
    covered_sum = 0
    start = time.perf_counter()
    for j in range(1):
        result_sets, lenth, covered_len, c = RUN.main(add_elements.copy(),all_sets.copy())        
        cpu = c*15+(total_cpu-c)*10       
        cpu_sum = cpu + cpu_sum
        covered_sum = covered_len + covered_sum       
    end = time.perf_counter()
    timeneed = end - start
    timeneed_av = timeneed/1
    cpu_av = cpu_sum//1
    covered_av = covered_sum//1
    formated_time = '{:.15f}'.format(timeneed_av)
    time_array.append(formated_time)
    print("cpu: ", cpu_av)
    cpu_array.append(cpu)
    print("total cpu: ",total_cpu*10)
    totalcpu_array.append(total_cpu)
    print("total paths: ", len(S), " ", covered_av)
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
        
        
        
    



