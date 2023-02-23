import re
import time
from random import choice
import linecache

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
    def main(self, all_elements, all_sets):
        lenth = len(all_sets)
        start = time.time()
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
        end = time.time()
        timeneed = end - start
        covered_len = len(final_all_sets)
        cpu = 0
        result_sets = {}
        for path in final_all_sets:
            cpu = cpu + len(all_sets.get(path))
            result_sets[path] = all_sets.get(path)
        return result_sets,lenth, covered_len, cpu
    def get_points(self):
        begin_line = 1    
        data_path = r'points0.2(100).txt' 
        all_points = {}
        for i in range(100):
            content = linecache.getline(data_path, i+1).strip('\n')
            point = re.findall(r"\d+",content)
            point_int = set()
            for e in point:
                point_int.add(int(e))
            all_points[i] = point_int
            begin_line+=1
        return all_points
    def save_points(self,all_elements,n, times, change,filename): 
        time = 1
        selected = {}
        for i in range(times):
            print(selected)
            add_elements = set() 
            if time ==1:
                for j in range(n):
                    e = str(choice(list(all_elements)))
                    while e in add_elements:
                        e = str(choice(list(all_elements)))
                    add_elements.add(e)
                    with open(filename,"a") as ff:
                        ff.write(e+" ")   
            if time != 1:
                last= selected.get(time-1).copy()
                change_num = int(change*len(last))
                print(change_num)
                for j in range(change_num):
                    need_remove = choice(list(last))
                    last.remove(need_remove)
                    print(last)
                    e = str(choice(list(all_elements)))
                    while e in last:
                        e = str(choice(list(all_elements)))
                    add_elements.add(e)
                for u in last:
                    add_elements.add(u)
                for u in add_elements:
                    with open(filename,"a") as ff:
                        ff.write(u+" ")   
            with open(filename,"a") as f2:   
                f2.write("\n")    
            selected[time] = add_elements
            time+=1
                
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
all_all_sets,all_all_elements= RUN.read_file()
for key,value in all_all_sets.items():
    if key == 90:
        S = value
        E = all_all_elements.get(key)
# RUN.save_points(E.copy(),round(len(E)*0.2), 100,0.0625, "points0.2(100).txt")

total_cpu=0
for u in range(len(S)):
    total_cpu = total_cpu +len(S.get("path"+str(u)))     
all_points = RUN.get_points()
results = {}
result = {}
total_time=0
total_diff=0
total_l=0
total_cpu=0
for i in range(100):
    all_sets = S.copy()
    all_elements = E.copy()
    add_elements = all_points.get(i)
    start = time.time()
    result_sets, lenth, covered_len, c = RUN.main(add_elements,all_sets)
    end = time.time()
    timeneed = end - start
    results[i] = result_sets
    if i-1<0:
        result1 = {}
    else:
        result1 = results.get(i-1)
    result2 = results.get(i)
    l,p = RUN.get_gap(result1, result2)
    print("RunPeriod:",timeneed)
    print("cpu: ", c,"/",total_cpu,"dfference：",l,"(",p,"roads)")
    print ("input roads amount: ",lenth, " cover needed roads: ",  covered_len)
    print("=====================time point: ",i,"====================")
    total_time+=timeneed
    total_diff+=l
    total_l+=p
    total_cpu+=c
p_time= total_time/100
p_diff=total_diff/100
p_l = total_l/100
p_cpu = total_cpu/100
print("time: ",p_time)    
print("difference: ",p_diff)    
print("roads: ",p_l) 
print("cpu: ",p_cpu)        
        
        
        
        
        




