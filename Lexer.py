__author__ = 'Artiom.Casapu'

import re

token_definition = {
    'NUMBER': (r'[0-9]*', 1),
    'IDENTIFICATOR': ('[a-zA-Z_][a-zA-Z0-9_]*', 2),
    'IF': (r'if', 3),
    'WHILE': (r'while', 4),
    'MTOE': (r'=>', 5),
    'EQUALS': (r'==', 6),
    'LTOE': (r'<=', 7),
    'LT': (r'<', 8),
    'GT': (r'>', 9),
    'MOD': (r'%', 10),
    'LSQBR': (r'[', 11),
    'RSQBR': (r']', 12),
    'STRING_CONST': (r'"<any_character_here>"', 13),
    'STRING_TYPE': (r'string',14),
    'INTEGER_TYPE': (r'integer',15),
    'DOUBLE_TYPE': (r'double',16)
}


"""
    Symbol table example:

    Program structure example:


"""
class Lexer:

    def Lexer(self, token_definition, input):
        self.token_definition = token_definition
        self.symbol_table = dict()
        self.program_structure = dict()
        self.parse(input.split('\n \t'))

    def get_token(self, input, pos):
        for key in self.token_definition:
            m = re.match(self.token_definition[key][0], input, pos)
            if m is not None:
                return m
        return None


    def parse(self):
        pos = 0
        pass

    def getSymbolTable(self):
        pass

    def getProgramStructure(self):

    pass

input1 = """
"""

input2 = """
"""

input3 = """
"""