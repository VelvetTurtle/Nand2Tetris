# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:52:38 2021

@author: velve
"""
from constants import symbols
from constants import keywords
from constants import lexical_elements
import itertools
import collections
import re
class JackTokenizer:
    #constructor
    def __init__(self,input_file):
        file = open(input_file, 'r')
        self.input = file.read()
        file.close()
        self.tokens = collections.deque()
        self.current_token = None
        self.next_token = None
        self.current_token_type = None
        self.process_input()
        self.has_more_tokens = True
    def advance(self):
        if self.current_token == None:
            self.current_token = self.tokens.popleft()
        else:
            self.current_token = self.next_token
        if len(self.tokens) > 0:
            self.next_token = self.tokens.popleft()
        else:
            self.has_more_tokens = False
        self.current_token_type = self.token_type(self.current_token)
        print(self.current_token)
        print(self.current_token_type)
    def process_input(self):
        self.input = self.remove_white_space_and_comments()
        self.split(self.input)
    def split(self,string):
        temp = re.findall(lexical_elements,self.input)
        match = list(itertools.chain(*temp))
        for m in match:
            if m:
                self.tokens.append(m)
        
    def remove_white_space_and_comments(self):
        inline_comment = re.compile('//.*\n')
        multiline_comment = re.compile("/\*.*?\*/", flags=re.S)
        remove_multiline = re.sub(multiline_comment, ' ', self.input)
        remove_inline = re.sub(inline_comment, '\n', remove_multiline)
        return remove_inline
    
    def token_type(self, token):
        if token in symbols:
            return "SYMBOL"
        elif token.isnumeric():
            return "INTEGER_CONSTANT"
        elif token in keywords:
            return "KEYWORD"
        elif token.isalnum():
            return "IDENTIFIER"
        else:
            return "STRING_CONSTANT"
    def keyword(self):
        return self.current_token
    def symbol(self):
        return self.current_token
    def indentifier(self):
        return self.current_token
    def int_val(self):
         return int(self.current_token)
    def string_val(self):
        temp = self.current_token.replace("\"", '')
        return temp
    def get_token_type(self):
        if self.current_token_type == None:
            return -1
        return self.current_token_type.lower()
    
if __name__ == "__main__":
    t = JackTokenizer("Main.jack")
    f = open("Main.xml","w")
    f.write("<token>\n")
    t.advance()
    while(t.has_more_tokens):
        f.write("<{}>{}</{}>\n".format(t.get_token_type(), t.current_token,t.get_token_type()))
        t.advance()
    f.write("</token>\n")
    f.close()