# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:53:32 2021

@author: velve
"""
from constants import operations
import constants
import JackTokenizer
class CompilationEngine():
    
    def __init__(self,file_name):
        print(file_name)
        self.tokenizer = JackTokenizer.JackTokenizer(file_name)
        self.file_name = file_name.replace('jack','xml')
        print(self.file_name)
        self.file = open(self.file_name, "w")
        self.statement_functions = {"let":self.compile_let,
                                "do":self.compile_do,
                                "if":self.compile_if,
                                "while":self.compile_while,
                                "return":self.compile_return}
        self.tokenizer.advance()
        self.compile_class('')
        self.close()
    #'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self,indent):
        self.file.write("{}<class>\n".format(indent))
        innerIndent = indent + '    '
        self.eat("class",innerIndent)
        self.eat(indent = innerIndent)
        self.eat('{',innerIndent)
        while self.tokenizer.keyword() in ["static","field"]:
            self.compile_class_var_dec(innerIndent)
        while self.tokenizer.keyword() in ["constructor", "method", "function"]:
            self.compile_subroutine(innerIndent)
        self.eat('}',innerIndent)
        self.file.write("{}</class>\n".format(indent))
    
    #('static'|'field') type varName(',' varName)* ';'
    def compile_class_var_dec(self,indent):
        self.file.write("{}<classVarDec>\n".format(indent))
        innerIndent = indent + '    '
        kind = self.write_enum(['static', 'field'],indent = innerIndent)
        t_type = self.write_enum(['int','char','boolean'],"identifier",indent = innerIndent)
        self.eat(indent=innerIndent)
        while self.tokenizer.symbol() == ',':
            self.eat(',',innerIndent)
            self.eat(indent = innerIndent)
        self.eat(';',innerIndent)
        self.file.write("{}</classVarDec>\n".format(indent))
    def compile_subroutine(self,indent):
        self.file.write("{}<subroutine>\n".format(indent))
        innerIndent = indent + "    "
        self.write_enum(['method', 'constructor','function'],indent = innerIndent)
        self.write_enum(['void',"int",'char', 'boolean'], 'identifier',innerIndent)
        self.eat(indent = innerIndent)
        self.eat('(', innerIndent)
        self.compile_parameter_list(innerIndent)
        self.eat(')', innerIndent)
        self.eat('{',innerIndent)
        while self.tokenizer.keyword() == 'var':
            self.compile_var_dec(innerIndent)
        self.compile_statements(innerIndent)
        self.eat('}',innerIndent)
        self.file.write("{}</subroutine>\n".format(indent))
    
    #((type varName))(',' type varName)*)?
    def compile_parameter_list(self,indent):
        self.file.write("{}<parameterList>\n".format(indent))
        innerIndent = indent + "    "
        if self.tokenizer.get_token_type() == "identifier" or self.tokenizer.keyword() in ["int","char","boolean"]:
            self.write_enum(['int','char','boolean'], 'indentifier', innerIndent)
            self.eat(indent= innerIndent)
            while self.tokenizer.symbol() == ',':
                self.eat(',',innerIndent)
                self.write_enum(['int','char','boolean'], 'indentifier', innerIndent)
                self.eat(indent = innerIndent)
        self.file.write("{}</parameterList>\n".format(indent))
            
    #'var' type varName (',' varName)* ';'
    def compile_var_dec(self,indent):
        self.file.write("{}<varDeclaration>\n".format(indent))
        innerIndent = indent+ "    "
        kind = "var"
        self.eat(kind,innerIndent)
        t_type = self.write_enum(['void',"int",'char', 'boolean'], 'identifier',innerIndent)
        self.eat(indent = innerIndent)
        while self.tokenizer.symbol() ==',':
            self.eat(',',innerIndent)
            self.eat(indent = innerIndent)
        self.eat(";",innerIndent)
        self.file.write("{}</varDeclartion>\n".format(indent))
    def compile_do(self,indent):
        self.file.write("{}<doStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("do",innerIndent)
        self.eat(indent = innerIndent)
        if self.tokenizer.symbol() == '(':
            self.eat('(',innerIndent)
            self.compile_expression_list(innerIndent)
            self.eat(')',innerIndent)
        elif self.tokenizer.symbol() == '.':
            self.eat('.',innerIndent)
            self.eat(indent = innerIndent)
            self.eat('(',innerIndent)
            self.compile_expression_list(innerIndent)
            self.eat(')',innerIndent)
        self.eat(";",innerIndent)
        self.file.write("{}</doStatement>\n".format(indent))
    
    def compile_let(self,indent):
        self.file.write("{}<letStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("let",innerIndent)
        self.eat(indent = innerIndent)
        if self.tokenizer.symbol() == '[':
            self.eat('[',innerIndent)
            self.compile_expression(innerIndent)
            self.eat(']',innerIndent)
        self.eat("=", innerIndent)
        self.compile_expression(indent = innerIndent)
        self.eat(';',innerIndent)
        self.file.write("{}</letStatement>\n".format(indent))
    
    def compile_while(self,indent):
        self.file.write("{}<whileStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("while",innerIndent)
        self.eat("(",innerIndent)
        self.compile_expression(innerIndent)
        self.eat(")",innerIndent)
        self.eat("{",innerIndent)
        self.compile_statements(innerIndent)
        self.eat("}",innerIndent)
        self.file.write("{}</whileStatement>\n".format(indent))
    
    def compile_return(self, indent):
        self.file.write("{}<returnStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("return",innerIndent)
        if self.tokenizer.symbol() != ";":
            self.compile_expression(innerIndent)
        self.eat(";",innerIndent)
        self.file.write("{}</returnStatement>\n".format(indent))
    
    def compile_if(self,indent):
        self.file.write("{}<ifStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("if",innerIndent)
        self.eat("(",innerIndent)
        self.compile_expression(innerIndent)
        self.eat(")",innerIndent)
        self.eat("{",innerIndent)
        self.compile_statements(innerIndent)
        self.eat("}",innerIndent)
        if(self.tokenizer.keyword() == "else"):
            self.eat("else",innerIndent)
            self.eat("{",innerIndent)
            self.compile_statements(innerIndent)
            self.eat("}",innerIndent)
        self.file.write("{}</ifStatement>\n".format(indent))
    
    def compile_expression(self,indent):
        self.file.write("{}<expression>\n".format(indent))
        innerIndent = indent + "    "
        self.compile_term(innerIndent)
        #if next token is an operator then it must be followed by a term
        while self.tokenizer.symbol() in operations:
            self.eat(self.tokenizer.symbol(), innerIndent)
            self.compile_term(innerIndent)
        self.file.write("{}</expression>\n".format(indent))
    
    def compile_term(self,indent):
        self.file.write("{}<term>\n".format(indent))
        innerIndent = indent + "    "
        print("compileTerm")
        print(self.tokenizer.current_token)
        tokenType = self.tokenizer.get_token_type()
        if tokenType in ["integer_constant", "string_constant"]:
            self.eat(indent= innerIndent)
        elif self.tokenizer.keyword() in ['true','false','null','this']:
            self.eat(indent=innerIndent)
        elif tokenType == 'identifier':
            self.eat(indent = innerIndent)
            #handles array syntax
            if self.tokenizer.symbol() == '[':
                self.eat('[',innerIndent)
                self.compile_expression(innerIndent)
                self.eat(']',innerIndent)
            elif self.tokenizer.symbol() == '(':
                self.eat('(',innerIndent)
                self.compile_expression_list(innerIndent)
                self.eat(')',innerIndent)
            elif self.tokenizer.symbol() == '.':
                self.eat('.',innerIndent)
                self.eat(indent = innerIndent)
                self.eat('(',innerIndent)
                self.compile_expression_list(innerIndent)
                self.eat(')',innerIndent)
        elif tokenType== 'symbol':
            if self.tokenizer.symbol() == '(':
                self.eat('(',innerIndent)
                self.compile_expression(innerIndent)
                self.eat(')',innerIndent)
            elif self.tokenizer.symbol() in constants.unary_op:
                self.eat(self.tokenizer.symbol(),innerIndent)
                self.compile_term(innerIndent)
        else:
            print("errror erorrton mcerrors complie term")
        self.file.write("{}</term>\n".format(indent))
    
    def compile_statements(self,indent):
        self.file.write("{}<statements>\n".format(indent))
        innerIndent = indent + "    "
        if self.tokenizer.keyword() not in self.statement_functions:
            self.print_error_message()
            return
        while self.tokenizer.keyword() in self.statement_functions:
            self.statement_functions[self.tokenizer.keyword()](innerIndent)
        self.file.write("{}</statements>\n".format(indent))
    
    def write_enum(self, valid_list = None, type_exception = None,indent = ""):
        if self.tokenizer.keyword() in valid_list or self.tokenizer.get_token_type() == type_exception:
            self.file.write("{}<{}>".format(indent,self.tokenizer.get_token_type()))
            self.file.write("{}".format(self.tokenizer.keyword()))
            self.file.write("</{}>\n".format(self.tokenizer.get_token_type()))
            temp = self.tokenizer.keyword()
            self.tokenizer.advance()   
            return temp
        else:
            self.print_error_message()
            return -1
    def close(self):
        self.file.close()
    
    def eat(self,string = None,indent = ""):
        self.file.write("{}<{}>".format(indent,self.tokenizer.get_token_type()))
        if self.tokenizer.symbol() in constants.symbol_conversions:
            self.file.write("{}".format(constants.symbol_conversions[self.tokenizer.symbol()]))
        elif self.tokenizer.get_token_type() == "string_constant":
            self.file.write("{}".format(self.tokenizer.string_val()))
        else:
            self.file.write("{}".format(self.tokenizer.current_token))
        self.file.write("</{}>\n".format(self.tokenizer.get_token_type()))
        self.tokenizer.advance()
    
    def compile_expression_list(self,indent):
        self.file.write("{}<expressionList>\n".format(indent))
        innerIndent = indent + "    "
        if self.tokenizer.get_token_type() != 'symbol':
            self.compile_expression(innerIndent)
            while self.tokenizer.symbol() == ',':
                self.eat(',',innerIndent)
                self.compile_expression(innerIndent)
        self.file.write("{}</expressionList>\n".format(indent))
    
    def print_error_message(self):
        print("Error: Unexpected Token.")
        print(self.tokenizer.current_token)