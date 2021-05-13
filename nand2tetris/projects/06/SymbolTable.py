# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 19:10:33 2021

@author: VelvetTurtle
"""

class SymbolTable():
    BUILT_IN_SYMBOLS = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576
        }
    def __init__(self):
        self.symbolTable = self.BUILT_IN_SYMBOLS
        self.nextAddress = 16
        
    def addEntry(self, symbol, address = None):
        print("S:",symbol)
        print("a:",address)
        print("nA:", self.nextAddress)
        if address:
            self.symbolTable[symbol] = address
        else:
            self.symbolTable[symbol] = self.nextAddress
            self.nextAddress += 1
    
    def contains(self, symbol):
        return symbol in self.symbolTable
    
    def getAddress(self, symbol):
        return self.symbolTable[symbol]
