__author__ = "Artiom.Casapu"

import operator

def read_file(filename):
    f = open(filename, 'r')
    result = f.read()
    f.close()
    return result

def write_symbol_table(symbol_table, out="symbol_table.txt"):
    f = open(out, 'w')

    sorted_x = []
    for x in symbol_table.key_set:
        sorted_x += [(x, symbol_table.get_value(x))]

    sorted_x = sorted(sorted_x, key = lambda x: x[1])

    for k,v in sorted_x:
        f.write("%d %s\n" % (v, k))
    f.close()

def write_fip(fip, out="fip.txt"):
    f = open(out, 'w')
    for k,v in fip:
        f.write("%d %d\n" % (k,v))
    f.close()
