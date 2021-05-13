# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 19:07:59 2021

@author: VelvetTurtle
"""
from hack_parser import Parser
from SymbolTable import SymbolTable
from hack_decoder import Code

#change this to change what file needs to be assembled
FILE_NAME = "Rect.asm"

class HackAssembler:
    def __init__(self,fileName):
        self.parser = Parser(fileName)
        self.symbolTable = SymbolTable()
        self.code = Code()
        self.fileName=fileName
    def execute(self):
        self.firstPass()
        self.finalPass()
   
    def firstPass(self):
        """
        uses parser to read the file and add the labels used for flow control
        to the symbol table class
        """
        instructionCount= 0 #count number of instructions,not including comments or L_COMMANDS
        while self.parser.hasMoreLines:
            self.parser.advance()
            instructionType = self.parser.instructionType()
            if self.parser.currentInstruction == '':
                continue
            if instructionType == "L_COMMAND":
                self.symbolTable.addEntry(self.parser.symbol(), address = instructionCount)
            elif instructionType == "NOT_COMMAND":
                continue
            else:
                instructionCount += 1
           
    def finalPass(self):
        self.parser.reset()
        writeFileName = self.fileName.split('.')[0] + ".hack"
        f = open(writeFileName, "w")
        writeLine = ""
        while self.parser.hasMoreLines:
            self.parser.advance()
            instructionType = self.parser.instructionType()
            if instructionType == "A_COMMAND":
                symbol = self.parser.symbol()
                writeLine = ""
                if not isNumber(symbol):
                    if not self.symbolTable.contains(symbol):
                        self.symbolTable.addEntry(symbol)
                    address = self.symbolTable.getAddress(symbol)
                else:
                    address = symbol
                temp = '{0:016b}'.format(int(address))
                writeLine += temp
            elif instructionType == "C_COMMAND":
                writeLine ="111"             
                writeLine += self.code.comp(self.parser.comp())
                writeLine += self.code.dest(self.parser.dest())
                writeLine += self.code.jump(self.parser.jump())
            else:
                continue
            f.write(writeLine + '\n')
        self.parser.close()
        f.close()
def isNumber(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
if __name__ == "__main__":
    fileName = FILE_NAME
    assembler = HackAssembler(fileName)
    assembler.execute()
    print("successfully done the thing")
