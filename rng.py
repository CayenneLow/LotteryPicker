import random

class Error(Exception):
    def __init__(self, error):
        super().__init__(error)

class Exhausted(Exception):
    def __init__(self, error):
        super().__init__(error) 

def RNG(min, max, nNum, seen):
    checks(min,max,nNum)
    # main logic
    for x in range(nNum):
        # no other numbers to pick from
        if len(seen) >= max-min+1:
            raise Exhausted("All numbers Exhausted")
            break
        returnList = seen
        # keep looping if it's a duplicate number
        while (1):
            num = random.randint(min, max)
            if num in returnList:
                exist = True
            else:
                exist = False
                # display num then add it to seen list
                returnList.append(num)
                break
    return returnList

def checks(min, max, nNum):
    # error handling
    if (max < min or min < 1):
        raise Error("Invalid Range")
    elif (nNum > max - min + 1):
        raise Error("Too many requested numbers")

