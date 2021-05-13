# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:20:52 2021

@author: VelvetTurtle
"""
from vm_parser import VMParser
from vm_code_writer import CodeWriter
import sys
import os
import glob
class Main:
    def __init__(self):
        self.writer = CodeWriter()
        self.read_files = []
        self.create_parser_objects()
    
    def create_parser_objects(self):
       files = self.get_files_to_be_translated()
       if files == None:
           print("Error file type not supported")
       self.read_files.append(VMParser(files))
       
    def get_files_to_be_translated(self):
        source_file = sys.argv[1]
        return source_file
    
    def execute(self):
        for file in self.read_files:
            self.writer.set_file_name(file.file_name)
            while file.has_more_commands:
                file.advance()
                command_type = file.command_type()
                print(command_type)
                if command_type == "arithmetic":
                    self.writer.write_arithmetic(file.operation())
                elif command_type == "comparison":
                    self.writer.write_comparison(file.operation())
                elif command_type == "pop" or command_type == "push":
                    self.writer.write_push_pop(file.operation(), file.segment(), file.index())
            file.close()
if __name__ == "__main__":
    main = Main()
    main.execute()
