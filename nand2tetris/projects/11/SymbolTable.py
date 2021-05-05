# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:51:32 2021

@author: velve
"""


class SymbolTable():
    def __init__(self):
        self.class_table = {}
        self.sub_table = {}
        self.id_count = {"static":0,
                         "field":0,
                         "argument":0,
                         "local":0}
    #clears out subroutine table and resets counts when exiting subroutine scope
    def start_subroutine(self):
        self.sub_table = {}
        self.id_count["argument"] = 0
        self.id_count["local"] = 0
    
    #uses kind to determine if class scope or subroutine scope
    def define(self,name,i_type, kind):
        if kind == "static" or kind == "field":
            self.add_to_table(self.class_table, name, i_type, kind)
        elif kind == "argument":
            self.add_to_table(self.sub_table,name, i_type, kind)
        elif kind == "var":
            self.add_to_table(self.sub_table,name,i_type,'local')
        else:
            print("Error, not a valid kind.")
            return
    #adds id to the passed table if its not already present 
    def add_to_table(self,table,name,i_type,kind):
        if name in table:
            print("Error duplicate var name in this scope")
        table[name] = [i_type,kind, self.id_count[kind]]
        self.id_count[kind] += 1
    
    def kind_of(self,name):
        if name in self.class_table:
            return self.class_table[name][1]
        elif name in self.sub_table:
            return self.sub_table[name][1]
        else:
            return None
    def type_of(self,name):
        if name in self.class_table:
            return self.class_table[name][0]
        elif name in self.sub_table:
            return self.sub_table[name][0]
        else:
            return None
    def index_of(self,name):
        if name in self.class_table:
            return self.class_table[name][2]
        elif name in self.sub_table:
            return self.sub_table[name][2]
        else:
            return None
    def number_of(self,kind):
        if kind == 'var':
            return self.id_count['local']
        return self.id_count[kind]