# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:20:52 2021

@author: velve
"""
from vm_parser import VMParser
from vm_code_writer import CodeWriter
import sys
import os
import glob
class Main:
    def __init__(self):
        self.w = CodeWriter()
        self.read_files = []
        self.create_parser_objects()
    def create_parser_objects(self):
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            self.read_files = [file_path]
            output_file_name = file_path.split('.')[0] + ".asm"
            self.w.set_file_name(output_file_name)

        elif os.path.isdir(file_path):
            vm_path = os.path.join(file_path, "*.vm")
            self.read_files = glob.glob(vm_path)
            output_file_name = os.path.basename(file_path)
            output_file_name = file_path + "/" + output_file_name + ".asm"
            self.w.set_file_name(output_file_name)
            self.w.write_init()
    def execute(self):
        for f in self.read_files:
            file = VMParser(f)
            while file.has_more_commands:
                file.advance()
                command_type = file.command_type()
                print(command_type)
                if command_type == "arithmetic":
                    self.w.write_arithmetic(file.operation())
                elif command_type == "comparison":
                    self.w.write_comparison(file.operation())
                elif command_type == "pop" or command_type == "push":
                    self.w.write_push_pop(file.operation(), file.segment(), file.index(),file.file_name)
                elif command_type == "goto":
                    self.w.write_goto(file.segment())
                elif command_type == "if-goto":
                    self.w.write_if(file.segment())
                elif command_type == "call":
                    self.w.write_call(file.segment(), file.index())
                elif command_type == "return":
                    self.w.write_return()
                elif command_type == "function":
                    self.w.write_function(file.segment(), file.index())
                elif command_type == "label":
                    self.w.write_label(file.segment())
            file.close()
if __name__ == "__main__":
    main = Main()
    main.execute()