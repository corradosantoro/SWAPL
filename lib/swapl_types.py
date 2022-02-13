# -----------------------------------------------------------------
# swapl_types.py
# -----------------------------------------------------------------

import random

from swapl_exceptions import *

# -----------------------------------------------------------------
class Set:

    def __init__(self, uData = []):
        self.data = uData

    def clone(self):
        cl = self.__class__
        cloned_data = [ ]
        for d in self.data:
            cloned_data.append(d)
        return cl(cloned_data)

    def __repr__(self):
        return repr(tuple(self.data))

    def __add__(self, other):
        res = self.clone()
        res.union(other)
        return res

    def __sub__(self, other):
        res = self.clone()
        res.difference(other)
        return res

    def _mklist(self, other):
        if isinstance(other, Set):
            return other.data
        elif isinstance(other, list):
            return other
        else:
            return [ other ]

    def size(self):
        return len(self.data)

    def union(self, other):
        data = self._mklist(other)
        for a in data:
            if not(a in self.data):
                self.data.append(a)

    def difference(self, other):
        data = self._mklist(other)
        for a in data:
            if a in self.data:
                self.data.remove(a)

    def items(self):
        return self.data

    def one(self):
        idx = random.randint(0, len(self.data) - 1)
        selected = Set([ self.data[idx] ])
        return selected

    def all(self):
        return self

    def roles(self, uRoleList):
        selected = [ ]
        for a in self.data:
            if a.get_field('role') in uRoleList:
                selected.append(a)

        return Set(selected)

    def all_but(self, term):
        return self - term

# -----------------------------------------------------------------
class OrderedSet(Set):

    def __init__(self, uData = []):
        super().__init__(uData)

    def __repr__(self):
        return repr(self.data)

    def __getitem__(self, idx):
        return self.get_item(idx)

    def union(self, other):
        data = self._mklist(other)
        for a in data:
            self.data.append(a)

    def get_item(self, uItemIndex):
        return self.data[uItemIndex]

    def set_item(self, uItemIndex, uItemData):
        self.data[uItemIndex] = uItemData

# -----------------------------------------------------------------
class StructData:

    def __init__(self, uKeys = [], uVals = []):
        self.data = { }
        for i in range(0, len(uKeys)):
            self.data[uKeys[i]] = uVals[i]

    def from_dict(self, dictionary):
        self.data = dictionary

    def clone(self):
        return StructData(list(self.data.keys()), [ self.data[x] for x in list(self.data.keys()) ])

    def __getitem__(self, item_key):
        return self.data[item_key]

    def __setitem__(self, item_key, item_data):
        self.data[item_key] = item_data

    def __repr__(self):
        return repr(self.data)

    def __add__(self, other):
        if isinstance(other, StructData):
            res = self.clone()
            for k in other.data.keys():
                res.data[k] = other.data[k]
            return res
        else:
            raise InvalidTypeException("Must be a struct")

    def fields(self):
        return self.data.keys()

    def set_field(self, uName, uVal):
        self.data[uName] = uVal

    def get_field(self, uName):
        try:
            return self.data[uName]
        except KeyError:
            return None

    def get_data(self):
        return self.data

# -----------------------------------------------------------------

import math

class PythonLink:

        def __init__(self, link):
            self.link = link

        def __repr__(self):
            return "@pythonlink %s" % (self.link)

        def eval_as_attribute(self):
            return eval(self.link)

# -----------------------------------------------------------------

if __name__ == "__main__":

    s1 = Set()
    s2 = Set([2,3,4])
    s3 = Set([4,5,6])
    s1.union([1,2,3])
    s1.union(s2)
    s4 = s1 + s2 + s3

    print(s1,s2,s3,s4)

    for i in range(0,10):
        print(s4.one())

