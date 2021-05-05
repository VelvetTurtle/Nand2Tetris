# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 18:37:50 2021

@author: velve
"""
class CodeWriter():
    #register mapping segments with the start of their registers
    #if key is number R starts at that address
    #if key is string than the value at that string points to the start of R
    segment_pointers = {"local": "LCL",
                        "argument": "ARG",
                        "this": "THIS",
                        "that": "THAT",
                        "temp": "5",
                        "pointer": "3"}
    
    arithmetic_commands = {"add": "M=M+D\n",
                           "sub": "M=M-D\n",
                           "neg": "M=-M\n",
                           "or": "M=M|D\n",
                           "not": "M=!M\n",
                           "and": "M=M&D\n"}
    
    #maps each comparison command to thier corisponding jump command
    comparison_commands = {"lt": "D;JLT\n",
                           "eq": "D;JEQ\n",
                           "gt": "D;JGT\n"}
    
    def __init__(self):
        self.label_count = 0
        self.f = None
        self.function_call_count = 0
    #allows functionallity to write to a new file
    def set_file_name(self, output_file):
        self.close()
        file_name = str(output_file)
        file_name = file_name.split(".")[0]
        self.file_name = file_name + ".asm"
        self.label_count = 0
        self.f = open(self.file_name, "w")
    #writes assembly code for add,sub,neg,or,not,and commands
    def write_arithmetic(self,command):
        #pop value from stack
        self.decrement_sp()
        #if operation requires 2 arguements
        if command in [ 'add', 'sub', 'and', 'or']:
            self.f.write("D=M\n")
            self.decrement_sp()
        self.f.write(self.arithmetic_commands[command])
        self.increment_sp()
    
    def write_comparison(self,command):
        label = "TRUE"+str(self.label_count)
        self.decrement_sp()
        self.f.write("D=M\n")#pop 1st value into D
        self.f.write("@SP\n")
        self.f.write("A=M-1\n")
        self.f.write("D=M-D\n")
        self.f.write("M=-1\n")#set defualt value to -1
        self.f.write("@"+label+'\n')
        self.f.write(self.comparison_commands[command])#if condition is fulfiled skip to end keeping -1 in M
        self.f.write("@SP\n")
        self.f.write("A=M-1\n")
        self.f.write("M=0\n")
        self.f.write("("+label+")\n")
        self.label_count += 1
        
    def write_push_pop(self, command, segment, index):
        if command == "push":
            if segment == "constant":
                self.f.write("@"+index+'\n')                
                self.f.write("D=A\n")
            elif segment in self.segment_pointers:
                self.find_segment_index(segment, index)
                self.f.write("D=M\n")
            elif segment == "static":
                file_name= self.file_name.split('.')[0]
                self.f.write("@"+file_name+'.'+index+'\n')
                self.f.write("D=M\n")
            self.push_command_on_stack()
        elif command == "pop":
            self.pop_command_into_register(segment, index)
        else:
            print("Not a push or pop command\n")
    
    #takes value found in D and places it onto stack then increments SP
    def push_command_on_stack(self):
        self.f.write("@SP\n")
        self.f.write("A=M\n")
        self.f.write("M=D\n")
        self.increment_sp()
    
    def increment_sp(self):
        self.f.write("@SP\n")
        self.f.write("M=M+1\n")
    
    #pops value from stack and places it into specified location
    def pop_command_into_register(self, segment, index):
        
        if segment == "static":
            self.decrement_sp()
            self.f.write("D=M\n")
            file_name= self.file_name.split('.')[0]
            self.f.write("@"+ file_name + "." +index+ "\n")
            self.f.write("M=D\n")
            return
        self.f.write("@" + index + "\n")
        self.f.write("D=A\n")
        self.f.write("@"+ self.segment_pointers[segment]+'\n')
        
        #if statement to determine if the index is being added to pointer inside of address or to the address itself
        if segment in ["this", "that", "local", "argument"]:
            self.f.write("D=M+D\n")
        else:
            self.f.write("D=A+D\n")
        self.f.write("@13\n") #use R13 as a temp variable
        self.f.write("M=D\n")#stores the location into R13 for future use
        self.decrement_sp()#decrement stack pointer
        self.f.write("D=M\n")
        self.f.write("@13\n")
        self.f.write("A=M\n")
        self.f.write("M=D\n")
        
    def decrement_sp(self):
        self.f.write("@SP\n")
        self.f.write("AM=M-1\n")

    #finds the value to be pushed to stack for segments that are in the segment_pointer dict
    def find_segment_index(self,segment, index):
        self.f.write("@"+index+"\n")
        self.f.write("D=A\n")
        self.f.write("@"+self.segment_pointers[segment]+"\n")
        if segment == "static" or segment == "pointer":
            self.f.write("A=D+A\n")
        else:
            self.f.write("A=M+D\n")    
    
    """
    Added functionallity for Project 8
    
    """
    def writeInit(self):
        self.f.write("@SP\n")
        self.f.write("M=256\n")
        self.writeCall("Sys.init", 0)
    def writeLabel(self, label):
        self.f.write("({})".format(label))
    
    def writeGoto(self, label):
        self.f.write("@{}".format(label))
        self.f.write("0;JMP")
    
    def writeIf(self, label):
        self.decrement_sp()
        self.write("A=M\n")
        self.write("D=M\n")
        self.write("@{}\n".format(label))
        self.write("D;JEQ\n")
    def writeCall(self, functionName, numArgs):
        return_label = ("{}.{}".format(functionName, self.function_call_count))
        self.function_call_count += 1
        #push return address
        self.f.write("@{}".format(return_label))
        self.f.write("D=A\n")
        self.push_command_on_stack()
        #push LCL, ARG, THIS, THAT
        for address in ["@LCL", "@ARG", "@THIS", "@THAT"]:
            self.f.write("@{}\n".format(address))
            self.f.write("D=M\n")
            self.push_command_on_stack()
        #ARG = SP-numArgs-5
        self.f.write("@SP\n")
        self.f.write("D=M\n")
        self.f.write("@{}\n".format(numArgs))
        self.f.write("D=D-A\n")
        self.f.write("@5\n")
        self.f.write("D=D-A\n")
        self.f.write("@ARG\n")
        self.f.write("M=D\n")
        #LCL = SP
        self.f.write("@SP\n")
        self.f.write("D=M\n")
        self.f.write("@LCL\n")
        self.f.write("M=D\n")
        #goto f
        self.writeGoto(functionName)
        #(return-address)
        self.writeLabel(return_label)
    
    def writeReturn(self):
        #FRAME = LCL
        self.f.write("@LCL\n")
        self.f.write("D=M\n")
        self.f.write("@13\n")
        self.f.write("M=D\n")
        #RET = *(FRAME-5)
        self.restore_calling_function(address=14,difference=5)
        #*ARG = pop()
        self.decrement_SP()
        self.f.write("A=M\n")
        self.f.write("D=M\n")
        self.f.write("@ARG\n")
        self.f.write("A=M\n")
        self.f.write("M=D\n")
        #SP = ARG+1
        self.f.write("@ARG\n")
        self.f.write("D=M+1\n")
        self.f.write("@SP\n")
        self.f.write("M=D\n")
        #THAT = *(FRAME-1)  THIS= *(FRAME-2), ARG=*(FRAME-3), LCL = *(FRAME-4)
        difference = 1
        for address in ["@THAT", "@THIS", "@ARG",  "@LCL"]:
            self.restore_calling_function(address, difference)
            difference+= 1
        #goto RET
        self.writeGoto(14)
    def restore_calling_function(self, address, difference):
        self.f.write("@13\n")
        self.f.write("D=M\n")
        self.f.write("@{}\n".format(difference))
        self.f.write("D=D-A\n")
        self.f.write("A=D\n")
        self.f.write("D=M\n")
        self.f.write("@{}\n".format(address))
        self.f.write("M=D\n")
    def writeFunction(self, functionName, numLocals):
        self.writeLabel(functionName)
        for i in range(numLocals):
            self.write_push_pop("push","constant", 0)
    def close(self):
        if self.f != None:
            self.f.close()