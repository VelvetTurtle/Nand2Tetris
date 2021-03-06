# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:03:55 2021

@author: VelvetTurtle
"""

class HCode:
    compMnemonics= {
        'None': '',
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101'
        }
    destMnemonics= {
        'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }
    jumpMnemonics = {
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    def dest(self, mnemonic):
        return self.destMnemonics[mnemonic]
    def comp(self, mnemonic):
        return self.compMnemonic[mnemonic]
    def jump(self, mnemonic):
        return self.jumpMnemonics[mnemonic]
