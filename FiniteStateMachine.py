__author__ = 'artiom'

import re

class State:
    def __init__(self, name, isfinal=True):
        self.isfinal = isfinal
        self.name = name

    def __eq__(self, other):
        return self.name == other.name and self.isfinal == other.isfinal

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        result = self.name
        return result

class FSM:
    def __init__(self, alphabet, acceptsEmtpy=False):
        self.alphabet = alphabet
        self.transitions = dict()
        self.states = set()
        self.initialstate = State("Root", isfinal=acceptsEmtpy)
        self.transitions[self.initialstate] = []

    def addState(self, state):
        self.states.add(state)
        self.transitions[state] = []

    def findState(self, name):

        for state in self.states:
            if state.name == name:
                return state

        if (name == "Root"):
            return self.initialstate

        return None

    def addTransition(self, transition, startingstate, finalstate):
        self.transitions[startingstate] += [(transition, finalstate)]

    def accepts(self, string):
        currentState = self.initialstate
        for i in range(len(string)):
            if (string[i] not in self.alphabet):
                raise Exception("Character not in alphabet " + string[i])
            transition = None
            for k in self.transitions[currentState]:
                m = re.match(k[0], string[i])
                if (m is not None):
                    transition = k

            if transition is None:
                return False, None

            currentState = transition[1]

        return currentState.isfinal, currentState

    def longestPrefix(self, string):
        currentState = self.initialstate
        result = ''
        current = ''

        for i in range(len(string)):
            if (string[i] not in self.alphabet):
                break

            transition = None

            for k in self.transitions[currentState]:
                m = re.match(k[0], string[i])
                if (m is not None):
                    transition = k

            if transition is None:
                break

            current += string[i]
            currentState = transition[1]

            if (currentState.isfinal):
                result = current

        return result

def read_state_definition(filename='fsm.txt'):
    currentlyReading = None

    alphabet = None
    states = []
    transitions = []
    final_states = []

    f = open(filename)
    for line in f:
        if (line.startswith('Alphabet:')):
            currentlyReading = 'alphabet'
        elif (line.startswith('States:')):
            currentlyReading = 'states'
        elif (line.startswith('Transitions:')):
            currentlyReading = 'transitions'
        elif (line.startswith('Final states:')):
            currentlyReading = 'final_states'
        else:
            if (currentlyReading == 'alphabet'):
                alphabet = line.strip()
            elif (currentlyReading == 'states'):
                states += [line.strip()]
            elif (currentlyReading == 'transitions'):
                transitions += [line.strip().split(' ')]
            elif (currentlyReading == 'final_states'):
                final_states += [line.strip()]

    fsm = FSM(list(alphabet))

    for state in states:
        if (state in final_states):
            fsm.addState(State(state))
        else:
            fsm.addState(State(state, isfinal=False))

    for trans in transitions:
        startstate, finalstate = trans[0].split('->')
        pattern = trans[1]
        fsm.addTransition(pattern, fsm.findState(startstate), fsm.findState(finalstate))

    return fsm

def display_states(fsm):
    print 'States:'
    for state in fsm.states:
        print state

def display_final_states(fsm):
    print 'Final states:'
    for state in fsm.states:
        if (state.isfinal):
            print state

def display_alphabet(fsm):
    print fsm.alphabet

def display_transitions(fsm):
    print 'Transitions:'
    for key in fsm.transitions.keys():
        print key, ': ',
        for v in fsm.transitions[key]:
            print '(', v[0], v[1], ')',
        print

def check_if_accepted(fsm):
    str = raw_input('Enter a string:')
    result, state = fsm.accepts(str)
    print result, state

def check_longest_prefix(fsm):
    str = raw_input('Enter a string:')
    result = fsm.longestPrefix(str)
    print result

def show_main_menu(fsm):
    while True:
        print '1 - Display states'
        print '2 - Final states'
        print '3 - Display transitions'
        print '4 - Display alphabet'
        print '5 - Check if accepted'
        print '6 - Find longest prefix'
        print 'Anything else - Stop'
        x = raw_input('Option:')
        if (x == '1'):
            display_states(fsm)
        elif (x == '2'):
            display_final_states(fsm)
        elif (x == '3'):
            display_transitions(fsm)
        elif (x == '4'):
            display_alphabet(fsm)
        elif (x == '5'):
            check_if_accepted(fsm)
        elif (x == '6'):
            check_longest_prefix(fsm)
        else:
            break

if __name__ == "__main__":
    #fsm = FSM('01ab')
    #
    #letterState = State('Letter', isfinal=False)
    #digitState = State('Digit')
    #
    #fsm.addState(letterState)
    #fsm.addState(digitState)
    #
    #fsm.addTransition(r'[ab]', fsm.initialstate, letterState)
    #fsm.addTransition(r'[ab]', letterState, letterState)
    #fsm.addTransition(r'[01]', letterState, digitState)
    #fsm.addTransition(r'[01]', digitState, digitState)
    #
    #
    #print fsm.accepts('aa00a')
    ##print fsm.accepts('ab12')
    ##print fsm.accepts('c')
    #print fsm.longestPrefix('aaabb1101aaa')
    #print fsm.accepts('0a')

    fsm = read_state_definition('cpp_fsm.txt')
    show_main_menu(fsm)