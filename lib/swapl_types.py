# -----------------------------------------------------------------
# swapl_types.py
# -----------------------------------------------------------------

import random

from swapl_exceptions import *

# -----------------------------------------------------------------
class AttributeInterface:

    def __init__(self, obj, aname):
        self.obj = obj
        self.name = aname

    def get(self):
        return getattr(self.obj, self.name)

    def set(self, val):
        setattr(self.obj, self.name, val)

# -----------------------------------------------------------------
class SWAPLObject:

    def __init__(self):
        self._attributes = {}

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, repr(self._attributes))

    def from_dict(self, dictionary):
        for k in dictionary:
            self._attributes[k] = dictionary[k]

    def to_dict(self):
        ret_val = { }
        for k in self._attributes:
            v = self._attributes[k]
            if isinstance(v, AttributeInterface):
                v = v.get()
            ret_val[k] = v
        return ret_val

    def add_attributes(self, uKeys = [], uVals = []):
        for i in range(0, len(uKeys)):
            self._attributes[uKeys[i]] = uVals[i]

    def add_attribute(self, name, val):
        self._attributes[name] = val

    def get_attribute(self, name):
        if name not in self._attributes:
            raise UndefinedAttributeException((name, self))
        return self._attributes[name]

    def set_attribute(self, name, val):
        if name not in self._attributes:
            raise UndefinedAttributeException((name, self))
        self._attributes[name] = val

    def clone(self):
        cloned = SWAPLObject()
        cloned.add_attributes(list(self._attributes.keys()), [ self._attributes[x] for x in list(self._attributes.keys()) ])
        return cloned


# -----------------------------------------------------------------
class Set(SWAPLObject):

    def __init__(self, uData = []):
        super().__init__()
        self.data = uData
        self.add_attribute("all", Set.all)
        self.add_attribute("one", Set.one)
        self.add_attribute("roles", Set.roles)

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

    def __getitem__(self, idx):
        return self.data[idx]

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
            if a.get_attribute('role') in uRoleList:
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
# class StructData(SWAPLObject):

#     def __init__(self, uKeys = [], uVals = []):
#         self.data = { }
#         for i in range(0, len(uKeys)):
#             self.data[uKeys[i]] = uVals[i]
#         super().__init__()

#     def methods(self):
#         return []

#     def attributes(self):
#         return self.data.keys()

#     def get_attribute(self, name):
#         return self.data[name]

#     def set_attribute(self, name, val):
#         self.data[name] = val
#         self.reload()

#     def from_dict(self, dictionary):
#         self.data = dictionary
#         self.reload()

#     def clone(self):
#         return StructData(list(self.data.keys()), [ self.data[x] for x in list(self.data.keys()) ])

#     def __getitem__(self, item_key):
#         return self.data[item_key]

#     def __setitem__(self, item_key, item_data):
#         self.data[item_key] = item_data
#         self.reload()

#     def __repr__(self):
#         return repr(self.data)

#     def __add__(self, other):
#         if isinstance(other, StructData):
#             res = self.clone()
#             for k in other.data.keys():
#                 res.data[k] = other.data[k]
#             return res
#         else:
#             raise InvalidTypeException("Must be a struct")

#     # def fields(self):
#     #     return self.data.keys()

#     # def set_field(self, uName, uVal):
#     #     self.data[uName] = uVal

#     # def get_field(self, uName):
#     #     try:
#     #         return self.data[uName]
#     #     except KeyError:
#     #         return None

#     def get_data(self):
#         return self.data

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

