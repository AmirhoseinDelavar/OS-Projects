from array import *


class utilities:
    def intToVitual(str):
        if str.__sizeof__() != 0:
            binary = '{0:016b}'.format(int(str))
            pagenum = binary[:8]
            pageoffset = binary[8:]
            return pagenum, pageoffset


class Ram:
    def __init__(self):
        self.mem = {}
        for i in range(65536):
            self.mem[i] = 'e'

    def save(self, data, po):

        for i in range(256):
            j = int('{0:08b}'.format(i) + po, 2)
            if self.mem[j] == 'e':
                self.mem[j] = data
                return '{0:08b}'.format(i)


class Pagetable:
    def __init__(self):
        self.table = {}
        for i in range(256):
            self.table[i] = 'e'

    def findphysical(self, pn):
        pn = int(pn, 2)
        if self.table[pn] == 'e':
            return None
        else:
            return self.table[pn]

    def addphysical(self, fn, pn):
        pn = int(pn, 2)
        self.table[pn] = fn


class Harddisk:
    def __init__(self):
        self.file = open("./store.bin", 'r')

    def find(self, virtualadd):
        lines = self.file
        for line0 in lines:
            if line0.split()[0] == virtualadd:
                return line0.split()[1]


class TLB:
    def __init__(self):
        self.table = {}
        self.size = 0

    def findphysical(self, virtual):
        virtual = int(virtual, 2)
        if virtual in self.table.keys():
            return self.table[virtual]
        else:
            return None

    def addphysical(self, phad, virtual):
        virtual = int(virtual, 2)
        if self.size <= 16:
            self.table[virtual] = phad
            self.size += 1


if __name__ == '__main__':
    # open input file
    file = open("./test.txt", "r")
    # open harddisk file
    harddisk = Harddisk()
    # create page table
    pagetable = Pagetable()
    # create ram
    ram = Ram()
    # create TLB
    tlb = TLB()
    # read and execute input line by line
    for line in file:
        pagenum, pageoffset = utilities.intToVitual(line.strip())
        # print virtual add
        print("Virtual Address:" + pagenum + pageoffset)
        physicaladd = tlb.findphysical(pagenum + pageoffset)
        if physicaladd is not None:
            print("hit tlb")
            indx = int(physicaladd, 2)
            if ram.mem[indx] == 'e':
                data = harddisk.find(pagenum + pageoffset)
                framenum = ram.save(data, pageoffset)
                pagetable.addphysical(framenum, pagenum)
                physicaladd = "{0}{1}".format(framenum, pageoffset)
                indx = int(physicaladd, 2)
            print("Physica Address:" + physicaladd)
            print("Data :" + ram.mem[indx])
        else:
            framenum = pagetable.findphysical(pagenum)
            if framenum is not None:
                print("hit page table")
                print(framenum)
                indx = int("{0}{1}".format(framenum, pageoffset), 2)
                if ram.mem[indx] == 'e':
                    data = harddisk.find(pagenum + pageoffset)
                    framenum = ram.save(data, pageoffset)
                    pagetable.addphysical(framenum, pagenum)
                    indx = int("{0}{1}".format(framenum, pageoffset), 2)
                print("Physica Address:" + framenum + pageoffset)
                print("Data :" + ram.mem[indx])
                tlb.addphysical(framenum + pageoffset, pagenum + pageoffset)
            # load from disk to mem
            else:
                print("hard found")
                # fetch data from disk
                data = harddisk.find(pagenum + pageoffset)
                # save it to empty mem
                framenum = ram.save(data, pageoffset)
                # update page table
                pagetable.addphysical(framenum, pagenum)
                print("Physica Address:" + framenum + pageoffset)
                indx = int("{0}{1}".format(framenum, pageoffset), 2)
                print("Data :" + ram.mem[indx])
                tlb.addphysical(framenum + pageoffset, pagenum + pageoffset)
            print()
    file.close()
    harddisk.file.close()
