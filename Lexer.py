__author__ = 'Artiom.Casapu'

import re

token_definition = {
    'NUMBER': (r'[0-9]+', 1),
    'IDENTIFICATOR': (r'[a-zA-Z_][a-zA-Z0-9_]*', 2),
    'IF': (r'if', 3),
    'WHILE': (r'while', 4),
    'MTOE': (r'=>', 5),
    'PLUS': (r'\+', 6),
    'EQUALS': (r'==', 6),
    'LTOE': (r'<=', 7),
    'GTOE': (r'>=', 8),
    'LT': (r'<', 9),
    'GT': (r'>', 19),
    'MOD': (r'%', 11),
    'EQ': (r'=', 12),
    'LSQBR': (r'\[', 12),
    'RSQBR': (r'\]', 13),
    'STRING_CONST': (r'"[a-zA-Z0-9_]*"', 14),
    'STRING_TYPE': (r'String',15),
    'INTEGER_TYPE': (r'Integer',16),
    'DOUBLE_TYPE': (r'Double',17)
}

keywords = ['if', 'while', 'String', 'Integer', 'Double']
constants = ['STRING_CONST', 'NUMBER']

"""
    Symbol table example:

    Program structure example:


"""
class Lexer:

    def __init__(self, token_definition, text):
        self.token_definition = token_definition
        self.symbol_table = dict()
        self.program_structure = []
        self.parse(filter(lambda x: x != '' and x is not None, re.split('\n| |\t', text)))

    def get_token(self, text, pos):
        if (pos >= len(text)):
            return None, None

        matches = []
        for key in self.token_definition:
            m,k = re.match(self.token_definition[key][0], text[pos:]), key
            if m is not None:
                matches += [(m.group(), k)]

        if len(matches) == 0:
            return None, None

        if len(matches) == 1:
            return matches[0]

        result = None, None
        for match in matches:
            if match[0] in keywords:
                return match
            if result[0] is None or (len(result[0]) < len(match[0])):
                result = match

        return result


    def parse(self, text):
        result = []
        for seq in text:
            pos = 0
            token, token_type = self.get_token(seq, pos)

            if (token == None and pos < len(seq)):
                raise Exception('Unrecognized token ' + seq[pos:])

            while pos < len(seq):
                result += [(token, token_type)]

                if (token_type in constants) or (token_type == 'IDENTIFICATOR'):
                    if not (self.symbol_table.has_key(token)):
                        value = len(self.symbol_table) + 1
                        self.symbol_table[token] = value

                    self.program_structure += [(token_definition[token_type][1], self.symbol_table[token])]
                else:
                    self.program_structure += [(token_definition[token_type][1], 0)]

                pos += len(token)
                token, token_type = self.get_token(seq, pos)

                if (token == None and pos < len(seq)):
                    raise Exception('Unrecognized token ' + seq[pos:])

        self.parse_result = result


input1 = """

func main() {

}

"""

input2 = """
"""

input3 = """
"""

l = Lexer(token_definition, input1)
print l.symbol_table
print l.program_structure