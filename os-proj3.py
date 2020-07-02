import random

CYLINDERS = 10
REQSIZE = 5


class disk:
    def __init__(self, header):
        self.header = header
        self.reqqueue = self.reqgen(REQSIZE)
        print(self.reqqueue)
        self.fifo()
        self.sstf()
        self.scan()
        self.cscan()
        self.look()
        self.clook()

    def reqgen(self, size):
        que = []
        for i in range(size):
            que.append(random.randrange(CYLINDERS))
        return que

    def mvcylndr(self, d0, d1):
        return abs(d0 - d1)

    def fifo(self):
        print("FIFO:")
        d0 = self.header
        d1 = self.reqqueue[0]
        headermvnt = self.mvcylndr(d0, d1)
        for i in range(REQSIZE - 1):
            d0 = self.reqqueue[i]
            d1 = self.reqqueue[i + 1]
            headermvnt += self.mvcylndr(d0, d1)
        print(headermvnt)

    def sstf(self):
        print("SSTF:")
        reqsclone = self.reqqueue.copy()
        reqsclone.append(self.header)
        nxt, headermvnt = self.gotocloset(reqsclone, self.header)
        while reqsclone.__len__() > 1:
            nxt, h = self.gotocloset(reqsclone, nxt)
            headermvnt += h
        print(headermvnt)

    def gotocloset(self, reqsclone, header):
        reqsclone.sort()
        indexofheader = reqsclone.index(header)
        l = -1
        r = -1
        if indexofheader - 1 > -1:
            l = self.mvcylndr(header, reqsclone[indexofheader - 1])
        if indexofheader + 1 < reqsclone.__len__():
            r = self.mvcylndr(header, reqsclone[indexofheader + 1])
        if l == -1:
            x = reqsclone[indexofheader + 1]
            reqsclone.remove(header)
            return x, r
        if r == -1:
            x = reqsclone[indexofheader - 1]
            reqsclone.remove(header)
            return x, l
        if r < l:
            x = reqsclone[indexofheader + 1]
            reqsclone.remove(header)
            return x, r
        else:
            x = reqsclone[indexofheader - 1]
            reqsclone.remove(header)
            return x, l

    def scan(self):
        print("SCAN:")
        headermvnt = 0
        reqsclone = self.reqqueue.copy()
        reqsclone.append(self.header)
        reqsclone.sort()
        ih = reqsclone.index(self.header)
        pre = self.header
        for nxt in reqsclone[ih:]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        headermvnt += self.mvcylndr(pre, CYLINDERS - 1)
        pre = CYLINDERS - 1
        for nxt in reversed(reqsclone[:ih]):
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        print(headermvnt)

    def cscan(self):
        print("C-SCAN:")
        headermvnt = 0
        reqsclone = self.reqqueue.copy()
        reqsclone.append(self.header)
        reqsclone.sort()
        ih = reqsclone.index(self.header)
        pre = self.header
        for nxt in reqsclone[ih:]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        headermvnt += self.mvcylndr(pre, CYLINDERS - 1)
        headermvnt += CYLINDERS
        pre = 0
        for nxt in reqsclone[:ih]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        print(headermvnt)

    def look(self):
        print("LOOK:")
        headermvnt = 0
        reqsclone = self.reqqueue.copy()
        reqsclone.append(self.header)
        reqsclone.sort()
        ih = reqsclone.index(self.header)
        pre = self.header
        for nxt in reqsclone[ih:]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        for nxt in reversed(reqsclone[:ih]):
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        print(headermvnt)

    def clook(self):
        print("C-LOOK:")
        headermvnt = 0
        reqsclone = self.reqqueue.copy()
        reqsclone.append(self.header)
        reqsclone.sort()
        ih = reqsclone.index(self.header)
        pre = self.header
        for nxt in reqsclone[ih:]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        for nxt in reqsclone[:ih]:
            headermvnt += self.mvcylndr(pre, nxt)
            pre = nxt
        print(headermvnt)


if __name__ == '__main__':
    disk(3)
