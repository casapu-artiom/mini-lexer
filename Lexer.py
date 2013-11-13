__author__ = 'Artiom.Casapu'

import re

token_definition = {
    'IDENTIFICATOR': (r'[a-zA-Z_][a-zA-Z0-9_]*', 1),
    'STRING_CONST': (r'"[a-zA-Z0-9_]*"', 2),
    'CHAR_CONST': (r'\'[a-zA-Z0-9_ ]*\'', 3),
    'NUMBER': (r'[0-9]+', 4),
    'REAL_NUMBER': (r'[0-9]+\.[0-9]+',5),
    'SEPARATOR': (r'\n| |\t',6),
    'INTEGER_TYPE': (r'Integer',7),
    'DOUBLE_TYPE': (r'Double',8),
    'STRING_TYPE': (r'String',9),
    'CHAR_TYPE': (r'Char', 10),
    'FUNC': (r'func', 11),
    'MAIN': (r'main', 12),
    'OPEN_ROUND_BRACKET': (r'\(',13),
    'CLOSE_ROUND_BRACKET': (r'\)',14),
    'SINGLE_QUOTE': (r'\'', 15),
    'DOUBLE_QUOTE': (r'\"', 16),
    'LSQBR': (r'\[', 17),
    'RSQBR': (r'\]', 18),
    'LEFT_CURLY_BRACKET': (r'{', 19),
    'RIGHT_CURLY_BRACKET': (r'}', 20),
    'READ': (r'read', 21),
    'WRITE': (r'write', 22),
    'PLUS': (r'\+', 23),
    'MINUS': (r'\-', 24),
    'DIVIDE': (r'\/', 25),
    'MULTIPLY': (r'\*', 26),
    'MOD': (r'\%', 27),
    'ASSIGN': (r'=', 28),
    'EQUALS': (r'==', 29),
    'LT': (r'<', 30),
    'GT': (r'>', 31),
    'GTOE': (r'>=', 32),
    'LTOE': (r'<=', 33),
    'COMMA': (r',', 34),
    'IF': (r'if', 35),
    'WHILE': (r'while', 36),
    'CONST': (r'const', 37)
}

keywords = ['IF', 'WHILE', 'STRING_TYPE', 'INTEGER_TYPE', 'DOUBLE_TYPE','CHAR_TYPE', 'FUNC', 'CONST', 'MAIN', 'READ', 'WRITE']
constants = ['STRING_CONST', 'NUMBER', 'REAL_NUMBER', 'CHAR_CONST']

characters = ['+', '-', '/', '*', '%', '(', ')', '[', ']', '{', '}' ,',']
ambiguous_characters = ['=', '>', '<']
separators = [' ','\t','\n']

"""

"""
class Lexer:

    def __init__(self, token_definition, text):
        self.token_definition = token_definition
        self.symbol_table = dict()
        self.program_structure = []
        self.parse(text)

    def isident(self, char):
        return  char.isalnum() or (char == '_')

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
            if match[1] in keywords:
                return match
            if result[0] is None or (len(result[0]) < len(match[0])):
                result = match

        return result


    def parse(self, text):
        result = []
        seq = text
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

    def parse_without_regexp(self, text):
        result = []
        i = 0
        while i < len(text):
            if (text[i].isalpha() or text[i] == '_'):
                ident = ""
                while (i < len(text) and self.isident(text[i])):
                    ident += text[i]
                    i += 1
                token, token_type = self.get_token(ident, 0)
                result += [(token, token_type)]
                continue

            if (text[i].isdigit()):
                num = ""
                while (i < len(text) and text[i].isdigit()):
                    num += text[i]
                    i += 1

                if (i < len(text) and text[i] == '.'):
                    num += text[i]
                    i += 1
                    while (i < len(text) and text[i].isdigit()):
                        num += text[i]
                        i += 1

                token, token_type = self.get_token(num, 0)
                result += [(token, token_type)]
                continue

            if (text[i] in characters):
                token, token_type = self.get_token(text[i], 0)
                result += [(token, token_type)]
                i += 1
                continue

            if (text[i] in ambiguous_characters):
                ch = text[i]
                i += 1
                if (i < len(text) and text[i] == '='):
                    ch += text[i]
                    i += 1
                else:
                    i += 1
                token, token_type = self.get_token(ch, 0)
                result += [(token, token_type)]
                continue

            if (text[i] in separators):
                token, token_type = self.get_token(text[i], 0)
                result += [(token, token_type)]
                i += 1
                continue

            if (text[i] == "'"):
                ch = "'"
                i += 1
                if (i < len(i) and self.isadmissiblechar(text[i])):
                    ch += text[i]
                    i += 1
                else:
                    i += 1

                if (i < len(i) and text[i] == "'"):
                    ch += "'"
                    i += 1
                else:
                    raise Exception('Unrecognized token at ' + text[i])

                continue

            if (text[i] == '"'):
                ch = '"'
                i += 1
                while (i < len(text) and self.isadmissiblechar(text[i])):
                    ch += text[i]
                    i += 1
                if (i < len(text) and text[i] == '"'):
                    ch += text[i]
                    i += 1
                token, token_type = self.get_token(ch, 0)
                result += [(token, token_type)]
                continue

            raise Exception('Unrecognized token at ' + text[i])

        self.parse_result = result

    def isadmissiblechar(self, ch):
        return ch.isalpha() or ch.isdigit() or ch == ' ' or ch == '_'


input1 = """

x = "abc"

func main() {
    x = x + 2.0
    y == x
}

"""

input2 = """
"""

input3 = """
"""

l = Lexer(token_definition, input1)
print l.parse_result
print l.symbol_table
print l.program_structure
print l.get_token('main', 0)