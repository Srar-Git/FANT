import sympy
import math
import time
from sympy import *
import operator
from random import choice
from collections import Counter

class random_recover:
    def __init__(self, param_l ,last_result, all_sets, all_elements, P, D, U, Pi, Di, Ui, S_p, X_p, All_p):
        self.all_sets = all_sets
        self.all_elements = all_elements
        self.last_result = last_result
        self.param_l = param_l
        self.P = P
        self.D = D
        self.U = U
        self.Pi = Pi
        self.Di = Di
        self.Ui = Ui
        self.S_p = S_p
        self.All_p = All_p
        self.X_p = X_p
    
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
    
    def getfixl(self):
        total_D_len = 0
        total_P_len = 0
        for i in range(0, 1000):
            Pi_set = self.Pi.get(i)
            Di_set = self.Di.get(i)
            if Pi_set is not None:
                Pi_len = len(Pi_set)
            else:
                Pi_len = 0
            if Di_set is not None:
                Di_len = len(Di_set)
            else:
                Di_len = 0
            total_D_len = total_D_len + Di_len
            total_P_len = total_P_len + Pi_len
            if total_P_len == 0:
                return 0
            if total_D_len < (total_P_len * self.param_l):
                return i    
        
    def runmainloop(self, input_elements, input_sets):
        origin_sets = input_sets.copy()
        final_solution_keys = set()
        Y = input_elements.copy()
        while Y:
            covered_lenth = {}
            for key, value in input_sets.items():
                covered = Y & value
                if len(covered) != 0:
                    covered_lenth[key] = len(covered)
            if covered_lenth:
                max_key = max(covered_lenth.items(), key=operator.itemgetter(1))[0]
            else:
                break
            Z = input_sets.get(max_key)               
            Q = Z & Y
            if len(Q) == 0:
                break
            l = self.get_l(len(Z&Y))
            p = choice(list(Q))
            self.S_p[p] = max_key
            self.put_in_P(p, l)
            self.put_in_U(p, l)            
            for key, value in list(input_sets.items()):
                if (p in value):
                    # define F+
                    F_plus = value                    
                    # define F(p)
                    Fp = {}
                    Fp[p] = F_plus                    
                    # define X(p)
                    self.X_p = {}
                    self.X_p[p] = Fp.get(p) & Y
                    final_solution_keys.add(key)
                    del input_sets[key]
                    for elements in value:
                        if elements in Y:
                            Y.remove(elements)                              
        final_solution = {}
        for key in final_solution_keys:
            final_solution[key] = origin_sets.get(key)
        self.last_result.update(final_solution)
        return final_solution,self.P,self.D,self.U,self.Pi,self.Di,self.Ui,self.X_p,self.S_p,self.All_p
    
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