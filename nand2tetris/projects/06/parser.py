# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:44:34 2021

@author: VelvetTurtle
"""
class HackParser:
    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.currentInstruction = None
        self.hasMoreLines = True
        self.nextLine = None
  
    def advance(self):
        #advances currentInstruction one line
        if self.currentInstruction == None:
            self.currentInstruction = self.file.readline()
        else:
            self.currentInstruction = self.nextLine
        #processes currentInstruciton to remove comments and whitespace
        self.currentInstruction= self.currentInstruction.strip()
        self.currentInstruction=self.currentInstruction.split('//')[0]
        self.curretnInstruction=self.currentInstruction.strip(' ')
        #advance next line to determine if hasMoreLines is true
        self.nextLine = self.file.readline()
        if self.nextLine == '':
            self.hasMoreLines = False
   
    def instructionType(self):
        if self.currentInstruction[0] == '@':
            return "A_COMMAND"
        elif self.currentInstruction[0] == '(':
            return "L_COMMAND"
        elif self.currentInstruction == '':
            return "NO_COMMAND"
        else:
            return "C_COMMAND"
  
    def getHasMoreLines(self):
        return self.hasMoreLines
 
    #returns mnemonic for destination bits for c instructions 
    def dest(self):
        if '=' not in self.currentInstruction:
            return 'null'
        return self.currentInstruction.split(" = ")[0]
 
    #returns mnemonic for jump bits for c instruction
    def jump(self):
        if ';' not in self.currentInstruction:
            return 'null'
        return self.currentInstruction.split(" ; ")[1]
  
    #splits currentInstruction and extracts comp mnemonic   
    def comp(self):
        if '=' not in self.curretnInstruction:
            return self.currentInstruction.split(" ; ")[0]
        return self.currentInstruction.split(" = ")[1]
    
    def symbol(self):
      if '@' in self.currentInstruction:
          return self.currentInstruction.replace('@', '')
      s= self.currentInstruction.replace('(', '')
      s = s.replace(')', '')
      return s
    def close(self):
        self.file.close()
        
