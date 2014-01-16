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
        self.rules[self.start] = [Rule(self.start, [start_symbol])]
        self.symbols.add(self.start)
        self.first_cache = {}
        self.follow_cache = {}

    def nullable(self, rules):

        for rule in rules:
            if ('#' in rule.rhs):
                return True

        return False

    def first(self, symbols, visited=dict()):
        if (not symbols):
            return set([])

        print '#', symbols
        if (self.first_cache.has_key(tuple(symbols))):
            return self.first_cache[tuple(symbols)]

        if (len(symbols) == 1):
            if (visited.get(symbols[0], False)):
                return set([])

            if (symbols[0] in self.terminal_symbols):
                visited[symbols[0]] = True
                self.first_cache[tuple(symbols)] = {symbols[0]}
                return self.first_cache[tuple(symbols)]

            elif (symbols[0] in self.symbols):
                visited[symbols[0]] = True
                if (not self.rules.has_key(symbols[0])):
                    self.rules[symbols[0]] = []

                Y = self.rules[symbols[0]]

                if (len(Y) == 0):
                    self.first_cache[tuple(symbols)] = set([])
                    return set([])

                result = set([])
                for y in Y:
                    result |= self.first(tuple(y.rhs), visited)

                self.first_cache[tuple(symbols)] = result
                return result

            else:
                return set([])

        result = set()

        if (not visited.get(symbols[0], False)):
            result = self.first(tuple([symbols[0]]), visited)

        is_nullable = self.nullable(self.rules.get(symbols[0], [Rule('', [])]))

        for i in range(1, len(symbols)):
            if (not is_nullable): break
            if (not visited.get(symbols[i], False)):
                result |= (self.first(tuple([symbols[i]]), visited))
                is_nullable = is_nullable and self.nullable(self.rules.get(symbols[i], Rule('', [])))

        self.first_cache[tuple(symbols)] = result
        return result


    def follow(self, symbol, visited=dict()):
        result = {'$'}
        visited[symbol] = True

        for nonterminal in self.rules:
            for rule in self.rules[nonterminal]:
                if (symbol in rule.rhs):
                    for i in range(0, len(rule.rhs)-1):
                        if (rule.rhs[i] == symbol):
                            tmp = self.first(rule.rhs[i+1:], dict())
                            if ('#' in tmp):
                                result |= (tmp - {'#'})
                                if (not visited.get(rule.lhs, False)):
                                    tmp = self.follow(rule.lhs, visited)
                                    result |= tmp
                            else:
                                result |= tmp
                    if (rule.rhs[-1] == symbol):
                        if (not visited.get(rule.lhs, False)):
                            result |= self.follow(rule.lhs, visited)

        return result

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

    def closure(self, I):
        J = set()

        for lritem in I:
            J.add(lritem)

        cont = True
        while cont:
            cont = False

            newJ = set()

            for rule,idx in J:
                newJ.add((rule, idx))

                if (idx >= len(rule.rhs)):
                    continue

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

        return self.closure(J)

    def get_items(self):
        if (grammar.start not in grammar.rules):
            return set()

        start = (grammar.rules[grammar.start][0], 0)
        first_set = set()
        first_set.add(start)
        result = [self.closure(first_set)]

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

    def __init__(self, grammar):

        self.grammar = grammar
        self.items = self.get_items()

        self.goto_table = {}
        self.action_table = {}

        for i in range(len(self.items)):

            for x in grammar.terminal_symbols:
                found = False

                for item,idx in self.items[i]:
                    if (idx >= len(item.rhs)):
                        continue
                    if (item.rhs[idx] == x):
                        tmp = self.goto(self.items[i], x)
                        for j in range(len(self.items)):
                            if tmp == self.items[j]:
                                #self.action_table.get(i, dict()).get(x, "")
                                if (not self.action_table.has_key(i)):
                                    self.action_table[i] = dict()

                                self.action_table[i][x] = ("s", j)

            for item, idx in self.items[i]:

                if (grammar.rules[grammar.start][0] == item and idx == len(item.rhs)):
                    if (not self.action_table.has_key(i)):
                        self.action_table[i] = dict()

                    self.action_table[i]['$'] = ['accept']

                if item.lhs == grammar.start: continue

                if idx == len(item.rhs):
                    if (not self.action_table.has_key(i)):
                        self.action_table[i] = dict()

                    tmp = grammar.follow(item.lhs, dict())

                    for a in tmp:
                        if (grammar.rules.has_key(item.lhs)):
                            self.action_table[i][a] = ("r", item)

            for x in grammar.symbols:
                if (x in grammar.terminal_symbols): continue

                tmp = self.goto(self.items[i], x)

                for j in range(len(self.items)):
                    if (tmp == self.items[j]) and (i != j):
                        if (not self.goto_table.has_key(i)):
                            self.goto_table[i] = dict()

                        self.goto_table[i][x] = j

    def try_parse(self, list):
        list.append('$')
        stack = [0]

        k = 0
        a = list[k]

        while True:
            s = stack[-1]

            if (not self.action_table.has_key(s)):
                print "ERROR"
                return

            if (not self.action_table[s].has_key(a)):
                print 'ERROR'
                return

            if (self.action_table[s][a][0] == 's'):
                stack.append(self.action_table[s][a][1])
                k = k + 1
                if (k >= len(list)):
                    print 'ERROR'
                    return
                a = list[k]

            elif (self.action_table[s][a][0] == 'r'):
                rule = self.action_table[s][a][1]
                for x in range(len(rule.rhs)):
                    stack.pop()
                t = stack[-1]
                stack.append(self.goto_table[t][rule.lhs])
                print rule

            elif (self.action_table[s][a][0] == 'accept'):
                print 'ACCEPTED'
                return

            else:
                print 'ERROR'
                return

    def construct_parse_tree(self):
        pass


if __name__ == "__main__":
    grammar_string = """
    E -> E + T | T
    T -> T * F | F
    F -> ( E ) | id
    """

    grammar_string_2 = """
    E -> T E'
    E' -> + T E' | #
    T -> F T'
    T' -> * F T' | #
    F -> ( E ) | id
    """
    grammar = Grammar(grammar_string, 'E')

    #print grammar.terminal_symbols
    #print grammar.symbols
    #print grammar.rules
    #print grammar.start

    parser = Parser(grammar)

    #print parser.items

    #print grammar.first("+", dict())

    #print parser.items
    #print parser.action_table
    #print parser.goto_table


    print parser.try_parse(['(','id', '+', 'id', ')', '+', 'id'])