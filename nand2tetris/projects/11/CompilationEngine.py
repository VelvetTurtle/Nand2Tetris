# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:53:32 2021

@author: velve
"""
from constants import operations
import constants
import JackTokenizer
import SymbolTable
import VMWriter
class CompilationEngine():
    
    def __init__(self,file_name):
        print(file_name)
        self.tokenizer = JackTokenizer.JackTokenizer(file_name)
        self.file_name = file_name.replace('jack','xml')
        print(self.file_name)
        self.file = open(self.file_name, "w")
        self.class_name = None
        self.statement_functions = {"let":self.compile_let,
                                    "do":self.compile_do,
                                    "if":self.compile_if,
                                    "while":self.compile_while,
                                    "return":self.compile_return}
        self.symbol_table = SymbolTable.SymbolTable()
        self.code_writer = VMWriter.VMWriter(file_name)
        self.tokenizer.advance()
        self.label_num = 0
        self.compile_class('')
        self.close()
        self.code_writer.close()
    #'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self,indent):
        self.file.write("{}<class>\n".format(indent))
        innerIndent = indent + '    '
        self.eat("class",innerIndent)
        self.class_name = self.tokenizer.identifier()
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
        #create variables temporarily storing the kind and type so the variable can be added to symboltable
        kind = self.write_enum(['static', 'field'],indent = innerIndent)
        t_type = self.write_enum(['int','char','boolean'],"identifier",indent = innerIndent)
        self.symbol_table.define(self.tokenizer.identifier(), t_type, kind)
        self.eat(indent=innerIndent)
        while self.tokenizer.symbol() == ',':
            self.eat(',',innerIndent)
            self.symbol_table.define(self.tokenizer.identifier(),t_type,kind)
            self.eat(indent = innerIndent)
        self.eat(';',innerIndent)
        self.file.write("{}</classVarDec>\n".format(indent))
    def compile_subroutine(self,indent):
        self.file.write("{}<subroutine>\n".format(indent))
        innerIndent = indent + "    "
        #reset the subroutine symbol table
        self.symbol_table.start_subroutine()
        #add this to symbol table for all new subroutines
        function_mod = self.write_enum(['method', 'constructor','function'],indent = innerIndent)
        self.write_enum(['void',"int",'char', 'boolean'], 'identifier',innerIndent)
        if function_mod == 'method':
            self.symbol_table.define("this",self.class_name,"argument")
        function_name = self.class_name+'.'+self.tokenizer.identifier()
        self.eat(indent = innerIndent)
        self.eat('(', innerIndent)
        self.compile_parameter_list(innerIndent)
        self.eat(')', innerIndent)
        self.eat('{',innerIndent)
        while self.tokenizer.keyword() == 'var':
            self.compile_var_dec(innerIndent)
        #write subroutine
        self.code_writer.write_function(function_name,self.symbol_table.number_of("var")) 
        if function_mod =='constructor':
            self.code_writer.write_push('constant',self.symbol_table.number_of('var'))
            self.code_writer.write_call('Memory.alloc',1)
            self.code_writer.write_pop('pointer',0)
        if function_mod =='method':
            self.code_writer.write_push('arguement',0)
            self.code_writer.write_pop('pointer',0)
        self.compile_statements(innerIndent)
        self.eat('}',innerIndent)
        self.file.write("{}</subroutine>\n".format(indent))
    
    #((type varName))(',' type varName)*)?
    def compile_parameter_list(self,indent):
        self.file.write("{}<parameterList>\n".format(indent))
        innerIndent = indent + "    "
        kind = "argument"
        if self.tokenizer.get_token_type() == "identifier" or self.tokenizer.keyword() in ["int","char","boolean"]:
            t_type = self.write_enum(['int','char','boolean'], 'identifier', innerIndent)
            self.symbol_table.define(self.tokenizer.identifier(),t_type,kind)
            self.eat(indent= innerIndent)
            while self.tokenizer.symbol() == ',':
                self.eat(',',innerIndent)
                t_type = self.write_enum(['int','char','boolean'], 'indentifier', innerIndent)
                self.symbol_table.define(self.tokenizer.identifier(),t_type,kind)
                self.eat(indent = innerIndent)
        self.file.write("{}</parameterList>\n".format(indent))
            
    #'var' type varName (',' varName)* ';'
    def compile_var_dec(self,indent):
        self.file.write("{}<varDeclaration>\n".format(indent))
        innerIndent = indent+ "    "
        kind = "var"
        self.eat(kind,innerIndent)
        t_type = self.write_enum(['void',"int",'char', 'boolean'], 'identifier',innerIndent)
        self.symbol_table.define(self.tokenizer.identifier(),t_type,kind)
        self.eat(indent = innerIndent)
        while self.tokenizer.symbol() ==',':
            self.eat(',',innerIndent)
            self.symbol_table.define(self.tokenizer.identifier(),t_type,kind)
            self.eat(indent = innerIndent)
        self.eat(";",innerIndent)
        self.file.write("{}</varDeclartion>\n".format(indent))
    def compile_do(self,indent):
        self.file.write("{}<doStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("do",innerIndent)
        subroutine_name = self.tokenizer.identifier()
        self.eat(indent = innerIndent)
        if self.tokenizer.symbol() == '(':
            self.eat('(',innerIndent)
            num_args = self.compile_expression_list(innerIndent)
            self.eat(')',innerIndent)
            num_args +=1
        elif self.tokenizer.symbol() == '.':
            self.eat('.',innerIndent)
            subroutine_name = subroutine_name +'.'+ self.tokenizer.identifier()
            self.eat(indent = innerIndent)
            self.eat('(',innerIndent)
            num_args = self.compile_expression_list(innerIndent)
            self.eat(')',innerIndent)
        self.eat(";",innerIndent)
        self.code_writer.write_call(subroutine_name, num_args)
        self.code_writer.write_pop('temp',0)
        self.file.write("{}</doStatement>\n".format(indent))
    
    def compile_let(self,indent):
        self.file.write("{}<letStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("let",innerIndent)
        variable = self.tokenizer.identifier()
        segment = self.symbol_table.kind_of(variable)
        index = str(self.symbol_table.index_of(variable))
        self.eat(indent = innerIndent)
        is_array = False 
        if self.tokenizer.symbol() == '[':
            is_array = True
            self.eat('[',innerIndent)
            self.compile_expression(innerIndent)
            self.code_writer.write_push(segment, index)
            self.code_writer.write_arithmetic('add')
            self.eat(']',innerIndent)
        self.eat("=", innerIndent)
        self.compile_expression(indent = innerIndent)
        if is_array:
            self.code_writer.write_pop('temp',0)
            self.code_writer.write_pop('pointer', 1)
            self.code_writer.write_push('temp',0)
            self.code_writer.write_pop('that',0)
        else:
            self.code_writer.write_pop(segment,index)
        self.eat(';',innerIndent)
        self.file.write("{}</letStatement>\n".format(indent))
    
    def compile_while(self,indent):
        self.label_num += 1
        self.file.write("{}<whileStatement>\n".format(indent))
        innerIndent = indent + "    "
        label = self.class_name+ '.' +str(self.label_num)+'.'+'L1'
        #label L1
        self.code_writer.write_label(label)
        self.eat("while",innerIndent)
        self.eat("(",innerIndent)
        #compiled(expression)
        self.compile_expression(innerIndent)
        #not
        self.code_writer.write_arithmetic("not")
        #if-goto L2
        label2 = self.class_name+'.'+str(self.label_num)+'.'+'L2'
        self.label_num += 1
        self.code_writer.write_if(label2)
        self.eat(")",innerIndent)
        self.eat("{",innerIndent)
        #compiled(statements)
        self.compile_statements(innerIndent)
        #goto L1
        self.code_writer.write_goto(label)
        self.eat("}",innerIndent)
        self.file.write("{}</whileStatement>\n".format(indent))
        #label L2
        self.code_writer.write_label(label2)
    def compile_return(self, indent):
        self.file.write("{}<returnStatement>\n".format(indent))
        innerIndent = indent + "    "
        self.eat("return",innerIndent)
        if self.tokenizer.symbol() != ";":
            self.compile_expression(innerIndent)
        else:
            self.code_writer.write_push('constant','0')
        self.eat(";",innerIndent)
        self.code_writer.write_return()
        self.file.write("{}</returnStatement>\n".format(indent))
    
    def compile_if(self,indent):
        self.label_num += 1
        self.file.write("{}<ifStatement>\n".format(indent))
        label = self.class_name + '.'+str(self.label_num)+'.'+'L1'
        label2 = self.class_name+'.'+str(self.label_num)+'.'+'L2'
        innerIndent = indent + "    "
        self.eat("if",innerIndent)
        self.eat("(",innerIndent)
        #compiled(expression)
        self.compile_expression(innerIndent)
        self.eat(")",innerIndent)
        #not
        self.code_writer.write_arithmetic("not")
        #if-goto L1
        self.code_writer.write_if(label)
        self.eat("{",innerIndent)
        #compiled(statements1)
        self.compile_statements(innerIndent)
        #goto L2
        self.code_writer.write_goto(label2)
        self.eat("}",innerIndent)
        #label L1
        self.code_writer.write_label(label)
        if(self.tokenizer.keyword() == "else"):
            self.eat("else",innerIndent)
            self.eat("{",innerIndent)
            #compiled(statements2)
            self.compile_statements(innerIndent)
            self.eat("}",innerIndent)
        #label L2
        self.code_writer.write_label(label2)
        self.file.write("{}</ifStatement>\n".format(indent))
    def compile_expression(self,indent):
        self.file.write("{}<expression>\n".format(indent))
        innerIndent = indent + "    "
        self.compile_term(innerIndent)
        #if next token is an operator then it must be followed by a term
        while self.tokenizer.symbol() in operations:
            operation = self.tokenizer.symbol()
            self.eat(self.tokenizer.symbol(), innerIndent)
            self.compile_term(innerIndent)
            if operation =='*':
                self.code_writer.write_call("Math.multiply",2)
            elif operation =='/':
                self.code_writer.write_call("Math.divide",2)
            elif operation in constants.operations_conversions:
                self.code_writer.write_arithmetic(constants.operations_conversions[operation])
        self.file.write("{}</expression>\n".format(indent))
    
    def compile_term(self,indent):
        self.file.write("{}<term>\n".format(indent))
        innerIndent = indent + "    "
        print("compileTerm")
        print(self.tokenizer.current_token)
        tokenType = self.tokenizer.get_token_type()
        if tokenType in ["string_constant"]:
            no_char = len(self.tokenizer.current_token)
            self.code_writer.write_push('constant', no_char)
            self.code_writer.write_call('String.new',1)
            for i in range(0, len(self.tokenizer.current_token)):
                self.code_writer.write_push('constant', ord(self.tokenizer.current_token[i]))
                self.code_writer.write_call('String.appendChar',2)
            self.eat(indent= innerIndent)
        elif tokenType == "integer_constant":
            self.code_writer.write_push('constant',self.tokenizer.int_val())
            self.eat(indent= innerIndent)
        elif self.tokenizer.keyword() in ['true','false','null','this']:
            if self.tokenizer.keyword() =='true':
                self.code_writer.write_push("constant",1)
                self.code_writer.write_arithmetic("neg")
            elif self.tokenizer.keyword() in ['false','null']:
                self.code_writer.write_push('constant',0)
            else:
                self.code_writer.write_push('pointer','0')
            self.eat(indent=innerIndent)
        elif tokenType == 'identifier':
            identifier = self.tokenizer.identifier()
            t = self.tokenizer.get_token_type()
            self.eat(indent = innerIndent)
            num_args =0
            #handles array syntax
            if self.tokenizer.symbol() == '[':
                index = self.symbol_table.index_of(identifier)
                segment = self.symbol_table.kind_of(identifier)
                
                self.code_writer.write_push(segment,index)
                
                self.eat('[',innerIndent)
                self.compile_expression(innerIndent)
                self.eat(']',innerIndent)
                
                self.code_writer.write_arithmetic('add')
                self.code_writer.write_pop('pointer',1)
                self.code_writer.write_push('that',0)
            elif self.tokenizer.symbol() == '(':
                self.eat('(',innerIndent)
                num_args = self.compile_expression_list(innerIndent)
                num_args +=1 
                self.eat(')',innerIndent)
                self.code_writer.write_call(identifier,num_args)
            elif self.tokenizer.symbol() == '.':
                self.eat('.',innerIndent)
                identifier = identifier +"."+ self.tokenizer.identifier()
                self.eat(indent = innerIndent)
                self.eat('(',innerIndent)
                num_args = self.compile_expression_list(innerIndent)
                self.eat(')',innerIndent)
                self.code_writer.write_call(identifier,num_args)
            else:
                index = self.symbol_table.index_of(identifier)
                segment = self.symbol_table.kind_of(identifier)
                self.code_writer.write_push(segment,index)
        elif tokenType== 'symbol':
            if self.tokenizer.symbol() == '(':
                self.eat('(',innerIndent)
                self.compile_expression(innerIndent)
                self.eat(')',innerIndent)
            elif self.tokenizer.symbol() in constants.unary_op:
                operator = self.tokenizer.symbol()
                self.eat(self.tokenizer.symbol(),innerIndent)
                self.compile_term(innerIndent)
                self.code_writer.write_arithmetic(constants.unary_op_conversions[operator])
                
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
        num_args = 0
        if self.tokenizer.get_token_type() != 'symbol':
            self.compile_expression(innerIndent)
            num_args += 1
            while self.tokenizer.symbol() == ',':
                self.eat(',',innerIndent)
                self.compile_expression(innerIndent)
                num_args +=1
        self.file.write("{}</expressionList>\n".format(indent))
        return num_args
    def print_error_message(self):
        print("Error: Unexpected Token.")
        print(self.tokenizer.current_token)