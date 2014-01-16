__author__ = 'artiom'

class Rule:

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def from_string(self, str):
        pass

    def __repr__(self):
        return "{" + str(self.lhs) + "->" + str(self.rhs) + "}"

    def __str__(self):
        return "{" + str(self.lhs) + "->" + str(self.rhs) + "}"

    def __hash__(self):
        result = 0

        if (self.lhs is not None):
            result += self.lhs.__hash__()

        if (self.rhs is not None):
 #           print "#", self.lhs, self.rhs
            result += tuple(self.rhs).__hash__()

        return result

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

class Grammar:

    def __init__(self, grammar_string, start_symbol):
        self.symbols = set([])
        self.terminal_symbols = set([])
        self.rules = self.extract_rules(grammar_string)
        self.start = start_symbol + "'"
        self.rules[self.start] = Rule(self.start, [start_symbol])
        self.first_cache = {}
        self.follow_cache = {}

    def nullable(self, rule):

        if ('#' in rule.rhs):
            return True

        return False

    def first(self, symbols, visited):
        if (not symbols):
            return set([])

        print '#', symbols
        if (self.first_cache.has_key(tuple(symbols))):
            return self.first_cache[tuple(symbols)]

        if (len(symbols) == 1):
            if (symbols[0] in self.terminal_symbols):
                self.first_cache[tuple(symbols)] = set([symbols[0]])
                return self.first_cache[tuple(symbols)]
            elif (symbols[0] in self.symbols):
                if (not self.rules.has_key(symbols[0])):
                    self.rules[symbols[0]] = []

                Y = self.rules[symbols[0]]

                if (len(Y) == 0):
                    self.first_cache[tuple(symbols)] = set([])
                    return set([])

                k = 1
                result = set([])
                result |= self.first(tuple(set(Y[0].rhs) - set(symbols) - set(visited.keys())), visited)

                for x in Y[0].rhs:
                    visited[x] = True

                while k < len(Y):
                    if (self.nullable(Y[k])):
                        for x in Y[k]:
                            visited[x] = True
                        result |= self.first(tuple(set(Y[k].rhs) - set(symbols) - set(visited.keys())), visited)
                    else:
                        break
                    k += 1

                self.first_cache[tuple(symbols)] = result
                return result

            else:
                return set([])

        visited[symbols[0]] = True
        result = self.first(tuple(set([symbols[0]]) - set(['#']) - set(visited.keys())), visited)
        is_nullable = self.nullable(self.rules.get(symbols[0], Rule('', [])))

        for i in range(1, len(symbols)):
            visited[symbols[i]] = True
            result |= (self.first(tuple(set([symbols[i]]) - set(['#']) - set(visited.keys())), visited))
            is_nullable = is_nullable and self.nullable(self.rules.get(symbols[i], Rule('', [])))

        self.first_cache[tuple(symbols)] = result
        return result


    def follow(self, symbols):
        pass

    def extract_rules(self, rules):
        result = {}

        for line in rules.splitlines():
            if (line.find("->") != -1):
                lhs, rhs = line.split("->")
                lhs = lhs.strip()

                options = []

                if (rhs.find("|") != -1):
                    for option in rhs.split("|"):
                        options.append(option)
                else:
                    options.append(rhs)

                for option in options:
                    if (not result.has_key(lhs)):
                        result[lhs] = []
                    result[lhs].append(Rule(lhs, option.split()))

                    self.symbols.add(lhs)
                    for x in option.split():
                        self.symbols.add(x)

        for x in self.symbols:
            if (not result.has_key(x)):
                self.terminal_symbols.add(x)

        return result

class ParseTree:
    def __str__(self):
        pass

class Parser:

    def closure(self, I, grammar):
        J = set()

        for lritem in I:
            J.add(lritem)

        cont = True
        while cont:
            cont = False

            newJ = set()

            for rule,idx in J:
                newJ.add((rule, idx))

                if (not grammar.rules.has_key(rule.rhs[idx])):
                    continue

                for prod in grammar.rules[rule.rhs[idx]]:
                    if (not (prod, 0) in J):
                        newJ.add((prod, 0))
                        cont = True

            J = newJ

        return J

    def goto(self, I, x):
        J = set()

        for rule, idx in I:
            if (idx >= len(rule.rhs)):
                continue
            if rule.rhs[idx] == x:
                J.add((rule, idx+1))

        return J

    def get_items(self, grammar):

        if (grammar.start not in grammar.rules):
            return set()

        start = (grammar.rules[grammar.start], 0)
        first_set = set()
        first_set.add(start)
        result = [self.closure(first_set, grammar)]

        cont = True
        while cont:
            cont = False

            for I in result:
                for X in grammar.symbols:
                    tmp = self.goto(I, X)
                    if (tmp and not (tmp in result)):
                        result.append(tmp)
                        cont = True

        return result

    def generate_parsing_table(self):
        pass

    def __init__(self, grammar):

        self.items = self.get_items(grammar)

        self.goto_table = {}
        self.action_table = {}

        for i in range(len(self.items)):
            for x in grammar.terminal_symbols:
                found = False

                for item,idx in self.items[i]:
                    if (idx >= len(item.rhs)):
                        continue
                    if (item.rhs[idx] == x):
                        found = True

                if (found):
                    tmp = self.goto(self.items[i], x)
                    for j in range(len(self.items)):
                        if tmp == self.items[j]:
                            #self.action_table.get(i, dict()).get(x, "")
                            if (not self.action_table.has_key(i)):
                                self.action_table[i] = {}

                            self.action_table[i][x] = "s" + str(j)


    def construct_parse_tree(self):
        pass


if __name__ == "__main__":
    grammar_string = """
    E -> E + T | T
    T -> T * F | F
    F -> ( E ) | id
    """
    grammar = Grammar(grammar_string, 'E')

    #print grammar.terminal_symbols
    #print grammar.symbols
    #print grammar.rules
    #print grammar.start

    parser = Parser(grammar)

    #print parser.items

    print grammar.first(['F'], dict())