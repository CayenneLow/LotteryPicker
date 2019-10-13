import random
from errors import *

def RNG(min, max, nNum, seen):
    checks(min,max,nNum)
    # main logic
    returnList = []
    for x in range(nNum):
        # no other numbers to pick from
        nSeen = 0
        for roll in seen:
            nSeen += len(roll)
        if nSeen >= max-min+1 or nSeen + len(returnList) >= max-min+1:
            break
        # keep looping if it's a duplicate number
        while (1):
            exist = False
            num = random.randint(min, max)
            if num in returnList:
                exist = True
            for roll in seen:
                if (num in roll):
                    exist = True
            if exist == False:
                # display num then add it to seen list
                returnList.append(num)
                break
    # returns list of new numbers
    return returnList

def checks(min, max, nNum):
    # error handling
    if (nNum <= 0):
        raise NegativeNNum("nNumbers must be greater than 0")
    if (max < min or min < 1):
        raise InvalidRange("Invalid Range")

