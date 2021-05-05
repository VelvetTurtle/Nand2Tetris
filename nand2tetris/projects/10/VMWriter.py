# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 19:01:35 2021

@author: velve
"""


class VMWriter:
    def __init__(self,output_file):
        self.file =open(output_file,"w")
    def write_push(self,segment,index):
        self.file.write("{} {} {}\n".format("push",segment,index))       
    def write_pop(self,segment,index):
        self.file.write("{} {} {}\n".format("pop",segment,index))    
    def write_arithmetic(self,command):
        self.file.write("{}\n".format(command))    
    def write_label(self, label):
        self.flie.write("{} {}\n".format("label",label))
    def write_goto(self, label):
        self.file.write("{} {}\n".format("goto",label))
    def write_if(self,label):
        self.file.write("{} {}\n".format("if-goto",label))
    def write_call(self,name,n_args):
        self.file.write("{} {} {}".format("call",name,n_args))
    def write_function(self,name,n_locals):
        self.file.write("{} {} {}".format("function",name,n_locals))
    def write_return(self):
        self.file.write("return\n")
    def close(self):
        self.file.close()