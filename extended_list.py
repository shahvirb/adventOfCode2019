import collections

class ExtendedList(collections.UserList):
    def __init__(self, data = []):
        collections.UserList.__init__(self)
        self.data = data

    def check_and_extend(self, i):
        # if i not in bounds of list will extend it
        index = i if type(i) is not slice else (i.stop - 1)
        if index >= len(self):
            self += [0] * (1 + index - len(self))

    def __getitem__(self, item):
        self.check_and_extend(item)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        self.check_and_extend(key)
        super().__setitem__(key, value)

    def __iter__(self):
        size = len(self)
        for i in range(super().__len__()):
            yield super().__getitem__(i)


def test():
    el = ExtendedList([i for i in range(5)])
    for i in range(len(el)):
        assert i == el[i]

    for i in el[0:2]:
        assert i == el[i]

    el[10] = -1
    assert el[10] == -1
    assert el[9] == 0