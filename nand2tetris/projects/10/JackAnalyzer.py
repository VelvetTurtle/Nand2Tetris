# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:52:38 2021

@author: velve
"""
import sys
import os
import CompilationEngine
import JackTokenizer
def main():
    if len(sys.argv) < 2:
        print("Error. No file or dir has been inputted")
        return -1
    if not os.path.exists(sys.argv[1]):
        print("Error: {} does not exist.".format(sys.argv[1]))
        return -1
    if os.path.isdir(sys.argv[1]):
        input_path = sys.argv[1]
        print("Input path:{}",input_path)
        compileFiles(input_path)
    else:
        input_file = sys.argv[1]
        compileFile(input_file)

def compileFile(input_path):
    ce = CompilationEngine.CompilationEngine(input_path)
def compileFiles(directory):
    for file in os.listdir(directory):
        if file.find('jack') != -1:
            compileFile(directory +'/'+ file)

if __name__ == '__main__':
    main()