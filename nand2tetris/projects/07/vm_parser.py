# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:00:18 2021

@author: Elizabeth Fox
"""

class VMParser():
    ARITHMETIC_COMMANDS = ["add",
                           "sub",
                           "neg",
                           "and",
                           "or",
                           "not"]
    COMPARISON_COMMANDS = ["lt",
                            "gt",
                            "eq"]
    def __init__(self, input_file):
        self.file_name = input_file
        self.file = open(self.file_name, 'r')
        self.current_command = None
        self.next_command = None
        self.has_more_commands = True
        self.split_command = None
    
    #remove comments and whitespace from current command
    def proccess_command(self, line):
        if line == None:
            return
        line = line.strip()
        line = line.split('//', 1)[0]
        line = line.strip()
        return line
    
    def advance(self):
        #advances current_command one line
        if self.current_command == None:
            self.current_command = self.file.readline()
        else:
            self.current_command = self.next_command
        #processes currentInstruciton to remove comments and whitespace
        self.current_command = self.proccess_command(self.current_command)
        #advance next line to determine if hasMoreLines is true
        self.next_command = self.file.readline()
        if self.next_command == '':
            self.has_more_commands = False
        self.split_commands(self.current_command)
        
    def command_type(self):
        if self.operation() in self.ARITHMETIC_COMMANDS:
            return "arithmetic"
        elif self.operation() in self.COMPARISON_COMMANDS:
            return "comparison"
        else:
            return self.operation()
        
    def split_commands(self, command):
        if command == None:
            return
        self.split_command = command.split(' ')
    
    def operation(self):
        return self.split_command[0]
    
    def segment(self):
        if len(self.split_command) != 3:
            return
        return self.split_command[1]
    
    def index(self):
        if len(self.split_command) != 3:
            return
        return self.split_command[2]
    
    def close(self):
        self.file.close()