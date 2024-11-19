#########
# Daniel Jaffe
# Date made 11/13/24
# This program emulates a virtual memory and shows the mapping from Virtual address to physical address
#########
import math
import random


# CPU
class CPU:
    def __init__(self):
        self.pageTable = PageTable()
        self.mainMemory = MainMemory()

    def main(self):
        file = (open("input1.txt", "r"))
        wasNewPrev = False
        # first line is words/instructions
        word = file.readline()
        # second line is number of pages
        maxpagesMainMemoryHolds = int(file.readline())
        amountBitsForPages = 0
        pageLevel = 0
        # go through file and determine what each line means
        for line in file:
            pageLevel += 1
            line = line.rstrip()
            # if NEW then new page table set wasnewprev to true
            if (line == "NEW"):
                wasNewPrev = True
            # if wasnewprev is true then this is the virtual memory number
            elif (wasNewPrev):
                virtualMemory = int(line)
                # print the results of the page fault
                pageFault = self.pageTable.getPageFaultsPercentage()
                print(f"{pageFault:.3f}%")
                # make a page table object that keeps track of size of page table
                self.pageTable.setPageTable(virtualMemory)
                # printing out the results of the pages
                previousPageTable = self.pageTable.getPageTable()
                allPages = self.mainMemory.addPageTable(previousPageTable)
                for i in range(0, len(allPages)):
                    print(' '.join(allPages[i]))
                print("\n")
                # Finds how many bits is for page number by doing a log to the base to of virtual memory
                # I read the math import file to see how to use log and ceiling function
                amountBitsForPages = math.ceil(math.log(virtualMemory, 2))
                wasNewPrev = False

            # otherwise it is an instruction
            else:
                # convert the page bits to a decimal
                pageNum = self.binConvertToDec(line[:amountBitsForPages])
                self.pageTable.placeNumber(pageNum, maxpagesMainMemoryHolds)
        # prints last page table with page fault
        pageFault = self.pageTable.getPageFaultsPercentage()
        previousPageTable = self.pageTable.getPageTable()
        allPages = self.mainMemory.addPageTable(previousPageTable)
        print(f"{pageFault:.3f}%")
        for i in range(0, len(allPages) - 1):
            print(' '.join(allPages[i]))
        print("\n")

    # Converts string page num from binary to decimal
    def binConvertToDec(self, stringNumber):
        total = 0
        stringNumberLength = len(stringNumber)
        for i in stringNumber:
            total += ((2 ** ((stringNumberLength - 1)) * (int(i))))
            stringNumberLength = stringNumberLength - 1
        return total


# Main memory
class MainMemory:
    def __init__(self):
        self.allPageTables = []

    # keeps track of all page tables
    def addPageTable(self, pageTable):
        self.allPageTables.append(pageTable)
        return self.allPageTables


# Page table
class PageTable:
    def __init__(self):
        self.total = 0
        self.misses = 0
        self.hits = 0

    def getPageTable(self):
        return self.pageTable

    def setPageTable(self, pageTableSize):
        self.pageTable = pageTableSize * ["_"]

    # places an index of main memory into page table
    def placeNumber(self, pageNumber, mainMemorySize):
        mainMemorytable = mainMemorySize * ["_"]
        openSpots = []
        # loop through the mainMemorytable to check if there is a something in that location
        for i in range(0, mainMemorySize):
            # if table doesn't have something in it add location to array
            if (mainMemorytable[i] == "_"):
                openSpots.append(i)
        # if page table at location of page number find a place to put it in main memory
        if self.pageTable[pageNumber] == "_":
            self.misses += 1
            # if open spots length is bigger than 0 add randomly pick a location
            if (len(openSpots) > 0):
                randomIndex = random.choice(openSpots)
                # place T in mainMemoryTable telling that there is something in that index
                mainMemorytable[randomIndex] = "T"
                # before placing number in page table check if number is already in page table
                self.pageTable = self.checkPageTable(self.pageTable, randomIndex, pageNumber)
            # otherwise main memory is full and randomly choice out of the size of the main memory
            else:
                randomIndex = random.randint(0, mainMemorySize - 1)
                # place T in mainMemoryTable telling that there is something in that index
                mainMemorytable[randomIndex] = "T"
                # before placing number in page table check if number is already in page table
                self.pageTable = self.checkPageTable(self.pageTable, randomIndex, pageNumber)
        # otherwise page table has a number in it and add one to hits
        else:
            self.hits += 1

    # checks page table for mainMemory location
    def checkPageTable(self, pageTable, randomIndex, pageNumber):
        for i in range(0, len(pageTable)):
            # if it is then remove it
            if (pageTable[i] == str(randomIndex)):
                pageTable[i] = "_"
        pageTable[pageNumber] = str(randomIndex)
        return pageTable

    # finds the page fault percentage
    def getPageFaultsPercentage(self):
        self.total = self.hits + self.misses
        # if the total is 0 return 0
        if (self.total == 0):
            return 0
        # else return the miss ratio
        return ((self.misses / self.total) * 100)


# Main
cpu = CPU()
cpu.main()
