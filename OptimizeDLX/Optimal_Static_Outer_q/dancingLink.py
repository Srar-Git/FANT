import operator
import re
import time
from random import choice
import linecache
import pdb

class dlx():
    def ini(self,rex,allsets_list):
        self.allsets_list = allsets_list
        self.sample = rex
        self.answer=[0]*len(self.sample)       
        self.n=len(self.sample[0])
        self.w=len(self.sample)       
        maxn = self.n*self.w
        self.L=[0]*maxn
        self.R=[0]*maxn
        self.U=[0]*maxn
        self.D=[0]*maxn
        self.nRow=[0]*maxn
        self.nCol=[0]*maxn
        self.vis = [0]*maxn
        self.S=[0]*maxn
        self.costH=[0]*maxn
        
        for i in range(0,self.w):
            line = 0
            for j in range(0,self.n):
                if self.sample[i][j]==1:
                    line+=1
            self.costH[i+1] = line
        self.allanswers={}
        self.answernum = 0
        self.vis = [0]*maxn
        self.best = 99999999
        self.danceCostMin = 9999999
                
        for i in range(0,self.n+1):
            self.L[i] = i-1
            self.R[i] = i+1
            self.U[i] = i
            self.D[i] = i
            self.nCol[i] = i
        self.L[0] = self.n
        self.R[self.n] = 0
        cnt = self.n+1
        for i in range(0,self.w):
            head = cnt
            tail = cnt
            for j in range(0, self.n):
                c = j+1
                if self.sample[i][j]==1:
                    self.S[c]+=1
                    print(cnt," ",len(self.nCol))
                    self.nCol[cnt] = c
                    self.nRow[cnt] = i+1                   
                    self.D[self.U[c]] = cnt
                    self.U[cnt] = self.U[c]  
                    self.D[cnt] = c
                    self.U[c] = cnt                   
                    self.L[cnt] = tail
                    self.R[tail] = cnt
                    self.R[cnt] = head
                    self.L[head] = cnt
                    tail = cnt
                    cnt+=1
        self.costc = self.Hash()
        self.ifDone = False

    def Remove(self, x):        
        i = self.D[x]
        while i!=x:           
            self.L[self.R[i]]= self.L[i]
            self.R[self.L[i]]= self.R[i]
            self.S[self.nCol[i]] = self.S[self.nCol[i]]-1            
            i = self.D[i]

    def Resume(self, x):     
        i = self.U[x]
        while i!=x:
            self.L[self.R[i]]= i
            self.R[self.L[i]]= i
            self.S[self.nCol[i]] +=1
            i = self.U[i]    

    def Hash(self):
        # change this inner q
        q = 0.001
        costmin = 0
        c = self.R[0]
        while c!=0:
            self.vis[c] = 1
            c = self.R[c]
        c = self.R[0]       
        count_loop = 0
        while c!=0:  
            tmpmin=999
            if self.vis[c]==1:
                count_loop+=1
                self.vis[c] = 0
                i = self.D[c]
                k = 0
                while i!=c:
                    k+=1
                    if tmpmin>self.costH[self.nRow[i]]:
                        tmpmin = self.costH[self.nRow[i]]
                    j = self.R[i]
                    while j!=i:
                        self.vis[self.nCol[j]] = 0
                        j=self.R[j]
                    i = self.D[i]
                tmpmin  = tmpmin # without optimize
                # tmpmin  = tmpmin * (k*p+(1-p))
                costmin = tmpmin + costmin
            c = self.R[c]
        costmin = costmin * (count_loop*q + (1-q)) # outer optimize the algorithm
        costmin = costmin 
        return costmin     

    def dfs(self,cost):
        if self.ifDone:
            return
        check = cost+self.Hash()
        if check >= self.costc:
            if check <= self.danceCostMin:
                self.danceCostMin = check
            return 
        if self.R[0]==0:
            self.answernum+=1
            self.allanswers["answer"+str(self.answernum)] = self.answer.copy()
            self.ifDone=True
            l = 0
            for e in self.answer:
                if e==1:
                   l+=1 
            cpu = 0
            index = 0
            for h in self.answer:
                if h ==1:
                    cpu = cpu + len(self.allsets_list[index])
                index+=1
            return
        minnum = 9999999999
        c= self.R[0]
        i = self.R[0]
        while i!=0:               
            if self.S[i] ==0:
                return
            if self.S[i] < minnum:
                minnum = self.S[i]
                c=i            
            i = self.R[i]        
        costsum = cost
        i = self.D[c]
        while i!=c:            
            self.answer[self.nRow[i]-1] = 1
            costsum+=self.costH[self.nRow[i]]
            self.Remove(i)
            j = self.R[i]
            while j!=i:
                self.Remove(j)
                j = self.R[j]
            self.dfs(costsum)
            j = self.L[i]
            while j!=i:
                self.Resume(j)
                j = self.L[j]
            self.Resume(i)
            self.answer[self.nRow[i]-1] = 0
            costsum=costsum - self.costH[self.nRow[i]]                
            i = self.D[i]

    def main(self, rex,allsets_list):
        self.ini(rex,allsets_list)
        start = time.perf_counter()
        for i in range(9999999999):
            if self.ifDone:
                break           
            self.dfs(0)
            if self.costc != self.danceCostMin+1:
                
                self.costc=self.danceCostMin+1
            else:
                self.costc+=1
            self.danceCostMin = 999999
        len_list = {}
        for index,ans in self.allanswers.items():
            lenth=0
            for i in range(0,len(ans)):
                if ans[i]==1:
                    lenth+=1
            len_list[index] = lenth
        min_len_key = min(len_list.items(), key=operator.itemgetter(1))[0]
        best = self.allanswers[min_len_key]
        cpu = 0
        index = 0
        for h in best:
            if h ==1:
                cpu = cpu + len(allsets_list[index])
            index+=1
        num = 0
        for a in best:
            if a ==1:
                num+=1
        end = time.perf_counter()
        timeneed = end - start
        return cpu,timeneed,num 
                  
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

    def get_points(self):
        begin_line = 1    
        data_path = r'points0.2.txt' 
        all_points = {}
        for i in range(8):
            content = linecache.getline(data_path, i+1).strip('\n')
            point = re.findall(r"\d+",content)
            point_int = set()
            for e in point:
                point_int.add(int(e))
                
            all_points[i] = point_int
            begin_line+=1
        return all_points    

# do the dlx set recover
DLX = dlx()
all_all_sets,all_all_elements= DLX.read_file()
path_array1 = []
all_all_points = DLX.get_points()
for key in all_all_sets.keys():
    if key!=1:
        path_array1.append(key)
time_array = []
totalcpu_array = []
cpu_array = []
path_array = []
for j in range(0,(len(path_array1))):
    if j==0:
        continue
    S = all_all_sets.get(j)
    for key,value in all_all_sets.items():
        if key == path_array1[j]:
            S = value
    all_points = all_all_points.get(j)
    total_cpu=0
    for u in range(len(S)):
        total_cpu = total_cpu +len(S.get(u)) 
    allsets_list=[]
    for p,sets in S.items():
        allsets_list.append(sets)
    all_element = all_points.copy()
    rexlines = [0]*len(all_element)
    rex = [0]*len(S)
    for i in range(0,len(S)):
        rex[i] = rexlines.copy()
    all_element_array = [0]*len(all_element)
    i = 0
    for e in all_element:
        all_element_array[i]= e
        i+=1
    line=0
    for key,value in S.items():
        for e in value:
            if e in all_element:
                index = all_element_array.index(e, 0,len(all_element_array))
                rex[line][index] = 1
        line+=1
    print(rex)
    cpu,timeneed,best = DLX.main(rex,allsets_list)
    print("RunPeriod:",timeneed)
    c = cpu*15+(total_cpu-cpu)*10
    print("cpu ",c,"/",total_cpu)
    print("input path amount: ",len(rex), " result path amount: ",best)
    print("")
    print("")
    formated_time = '{:.15f}'.format(timeneed)
    time_array.append(formated_time)
    cpu_array.append(c)
    totalcpu_array.append(total_cpu)
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









                    
    
                    
                    