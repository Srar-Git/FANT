import sympy
import scipy
import time
import math
from sympy import solve
from sympy.abc import x, y, z, a, b
from sympy import exp
import operator
from random import choice
from collections import Counter
from random_cover import random_recover

class dynamic_update:
    def __init__(self, param_l, all_elements, all_sets, add_elements, remove_elements, last_result, All_p, S_p, X_p, Orig_p, Extra_p, P, D, U, Pi, Di, Ui,A):
        self.add_elements = add_elements
        self.remove_elements = remove_elements
        self.last_result = last_result        
        self.param_l = param_l        
        self.all_elements = all_elements
        self.all_sets = all_sets        
        self.P = P
        self.D = D
        self.U = U
        self.Pi = Pi
        self.Di = Di
        self.Ui = Ui        
        self.All_p = All_p
        self.X_p = X_p
        self.S_p = S_p
        self.Orig_p = Orig_p
        self.Extra_p = Extra_p        
        self.A = A     
        
    def put_in_P(self, p, l):
        self.P[p] = l
        Pi_set = self.Pi.get(l)
        Pi_set.add(p)
        self.Pi[l] = Pi_set

    def put_in_U(self, p, l):
        self.U.add(p)
        Ui_set = self.Ui.get(l)
        Ui_set.add(p)
        self.Ui[l] = Ui_set

    def put_in_D(self, p, l):
        self.D.add(p)
        Di_set = self.Di.get(l)
        Di_set.add(p)
        self.Di[l] = Di_set
        
    def take_from_PDU(self, p):
        if p in self.P.keys():
            l = self.P.get(p)
            del self.P[p]
            if p in self.D:
                self.D.remove(p)
            if p in self.U:
                self.U.remove(p)
            Pi_set = self.Pi.get(l)
            if p in Pi_set:
                Pi_set.remove(p)
            self.Pi[l] = Pi_set
            Ui_set = self.Ui.get(l)
            if p in Ui_set:
                Ui_set.remove(p)
            self.Ui[l] = Ui_set
            Di_set = self.Di.get(l)
            if p in Di_set:
                Di_set.remove(p)
            self.Di[l] = Di_set

    def take_from_UD(self, p):
        l = self.P.get(p)
        del self.P[p]
        Pi_set = self.Pi.get(l)
        Pi_set.remove(p)
        self.Pi[l] = Pi_set
    
    def move_U_to_D(self,p):
        if p not in self.U:
            if p in self.D:
                return
        self.U.remove(p)
        self.D.add(p)
        l = self.P.get(p)
        Ui_set = self.Ui.get(l)
        Ui_set.remove(p)
        self.Ui[l] = Ui_set
        Di_set = self.Di.get(l)
        Di_set.add(p)
        self.Di[l] = Di_set    
            
    def get_l(self,lenth):
        if lenth is None or lenth == 0:
            return 0
        result_int = int(math.log(lenth,2))
        return result_int
    
    def get_maxS(self,S):
        lenth = {}
        for key, value in S.items():
            lenth[key] = len(value) 
            l_dict = {}
            for key, value in lenth.items():
                l = self.get_l(value)
                l_dict[key] = l
            max_S = max(l_dict.items(), key=operator.itemgetter(1))[0]
            return max_S
    
    def if_e_in_F(self, e, S):
        inF = False
        for key,value in self.last_result.items():
            if e in value:
                S[key] = value
                inF = True
            else:
                inF = False
        return inF, S
    
    def add_deal(self):
        if self.add_elements is None:
            return self.last_result
        Y = set()
        for e in self.add_elements:
            self.A.add(e)
            S = {}
            ifinF, S = self.if_e_in_F(e,S)
            if ifinF:
                maxS = self.get_maxS(S)
                if maxS in self.S_p.values():
                    p = list(self.S_p.keys())[list(self.S_p.values()).index(maxS)]
                    old_Extra_p = self.Extra_p.get(p)
                    if old_Extra_p is None:
                        old_Extra_p = set()
                    new_Extra_p = old_Extra_p.add(e)
                    self.Extra_p[p] = new_Extra_p
                    old_X_p = self.X_p.get(p)
                    if old_X_p is None:
                        old_X_p = set()
                    new_X_p = old_X_p.add(e)
                    self.X_p[p] = new_X_p
            else:
                Y.add(e)
        
        
        if Y:
            RC = random_recover(self.param_l, self.last_result, self.all_sets, Y, self.P, self.D,self.U, self.Pi, self.Di,self.Ui, self.S_p, self.X_p, self.All_p)
            RESULT,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p = RC.runmainloop(Y,self.all_sets)
            self.last_result.update(RESULT)
        return self.last_result,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p,self.A

    def remove_deal(self):
        if self.remove_elements is None:
            return self.last_result        
        for e in self.remove_elements:
            # if e in self.A:
            self.A.remove(e)
            if e in self.P.keys():
                self.move_U_to_D(e)
                D_len = len(self.D)
                P_len = len(self.P)
                # if len(self.D) > (self.param_l * len(self.P)):
                    # self.updating() 
        if len(self.D) > (self.param_l * len(self.P)): 
            self.updating() 
                   
    def getfixl(self):
        total_D_len = 0
        total_P_len = 0
        for i in range(0, 1000):
            Pi_set = self.Pi.get(i)
            Di_set = self.Di.get(i)
            if Pi_set is None:
                Pi_len = 0
            else:
                Pi_len = len(Pi_set)
            if Di_set is None:
                Di_len = 0
            else:
                Di_len = len(Di_set)
            total_D_len = total_D_len + Di_len
            total_P_len = total_P_len + Pi_len
            if total_D_len < (total_P_len * self.param_l):
                return i
    
    def updating(self):
        L = self.getfixl()
        if L is None:
            L = 0
        for p,lp in list(self.P.items()):
            if lp <= L: 
                flag = 0
                for key,value in list(self.last_result.items()):
                    if p in value:
                        del self.last_result[key]
                        flag = 1
                if flag == 1: 
                    self.take_from_PDU(p)
        X_ = set() #X'
        for e in self.A:
            for key1,value1 in self.last_result.items():
                if e not in value1:
                    X_.add(e)    
        #movement step
        for element in X_:
            seleceted_S = {}            
            SS = self.all_sets.copy()            
            for key3 in self.last_result.keys():
                if key3 in SS.keys():
                    del SS[key3]
            for key2,value2 in SS.items():
                if element in value2:
                    lenth = len(value2)
                    l = self.get_l(lenth)
                    if l > L:
                        seleceted_S[key2] = value2
            maxS = self.get_maxS(seleceted_S)
            if maxS in list(self.S_p.keys()):
                p = list(self.S_p.keys())[list(self.S_p.values()).index(maxS)]         
            old_Extra_p = self.Extra_p.get(p)
            if old_Extra_p is not None:
                new_Extra_p = old_Extra_p.add(e)
                self.Extra_p[p] = new_Extra_p
            old_X_p = self.X_p.get(p)
            if old_X_p is not None:
                new_X_p = old_X_p.add(e)
                self.X_p[p] = new_X_p            
        #covering step
        Y = X_.copy()
        S = {}
        for e in Y:
            for key,value in self.all_sets.items():
                if e not in value:
                    S[key] = value
        #run random cover
        RC = random_recover(self.param_l, self.last_result, S, Y, self.P, self.D,self.U, self.Pi, self.Di,self.Ui, self.S_p, self.X_p, self.All_p)
        RESULT,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p = RC.runmainloop(Y,S)
        self.last_result.update(RESULT)
        old_Orig_p = self.Orig_p.get(p)
        if old_Orig_p is not None:
            new_Orig_p = old_Orig_p.add(e)
            self.Orig_p[p] = new_Orig_p
        
    def get_P(self):
        return self.P
    
    def get_D(self):
        return self.D
    
    def get_U(self):
        return self.U
    
    def get_Pi(self):
        return self.Pi
    
    def get_Di(self):
        return self.Di
    
    def get_Ui(self):
        return self.Ui
    
    def get_X_p(self):
        return self.X_p
    
    def get_S_p(self):
        return self.S_p
    
    def get_All_p(self):
        return self.All_p
    
    def get_F(self):
        return self.last_result