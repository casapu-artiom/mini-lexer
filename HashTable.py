__author__ = 'artiom'

class HashTable:

    def __init__(self, max_capacity = 31117):

        self.capacity = max_capacity
        self.hash = [[] for i in range(self.capacity)]
        self.num = 0
        self.key_set = set()

    def hash_code(self, value):
        result = 0
        for i in range(len(value)):
            result = (result + 31 * ord(value[i])) % self.capacity
        return result

    def contains_key(self, key):
        h = self.hash_code(key)
        for i in range(len(self.hash[h])):
            if (self.hash[h][i][0] == key):
                return True
        return False

    def add_key(self, key, value):
        if self.contains_key(key):
            return

        self.key_set.add(key)

        h = self.hash_code(key)
        self.hash[h] += [(key, value)]
        self.num += 1


    def get_value(self, key):
        h = self.hash_code(key)
        for i in range(len(self.hash[h])):
            if (self.hash[h][i][0] == key):
                return self.hash[h][i][1]
        return None