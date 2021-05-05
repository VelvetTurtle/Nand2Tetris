# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 18:56:53 2021

@author: velve
"""
#sets for each of the token types
keywords = {"class",
            "constructor",
            "function",
            "method",
            "field",
            "static",
            "var",
            "int",
            "char",
            "boolean",
            "void",
            "true",
            "false",
            "null",
            "this",
            "let",
            "do",
            "if",
            "else",
            "while",
            "return"}
symbols = {'{',
           '}',
           '(',
           ')',
           '[',
           ']',
           '.',
           ',',
           ';',
           '+',
           '-',
           '*',
           '/',
           '&',
           '|',
           '<',
           '>',
           '=',
           '~'}
operations = {'+',
               '-',
               '*',
               '/',
               '&',
               '<',
               '>',
               '<',
               '>',
               '=',
               '-',
               '~',
               '|'}
operations_conversions = {'+':"add",
                          '-':"sub",
                          '~':"not",
                          '|':"or",
                          '&':"and",
                          '<':"lt",
                          '>':"gt"}
unary_op_conversions = {'-':"neg",
                        '~':"not"}
unary_op           = {'-',
                      '~'}
comment_operators  = {"/",
                      "*"}
symbol_conversions = {'<': '&lt;',
                      '>': '&gt;',
                      '\"': '&quot;',
                      '&': '&amp;'}
# regex strings to seperate file into tokens
re_symbol        = '([{}()[\].,;+\-*/&|<>=~])'
re_int_const     = '(\d+)'
re_string_const  = '\"([^\n]*)\"'
re_indentifer    = '([A-Za-z_]\w*)'
lexical_elements = '{}|{}|{}|{}'.format(re_symbol, re_int_const,
                                           re_string_const, re_indentifer)