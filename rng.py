import random

class Error(Exception):
    def __init__(self, error):
        super().__init__(error)

# global seen list for checking duplicates
seen = []
def RNG(min, max, nNum, iteration):
    # error handling
    if (max < min or min < 1):
        raise Error("Invalid Range")
    elif (nNum > max - min + 1):
        raise Error("Too many requested numbers")
    # main logic
    for x in range(nNum):
        # no other numbers to pick from
        if len(seen) >= max-min+1:
            print("All numbers exhausted")
            break

        # keep looping if it's a duplicate number
        num = -1
        exist = True
        while (exist == True):
            num = random.randint(min, max)
            if num in seen:
                exist = True
            else:
                exist = False
        # display num then add it to seen list
        print(num)
        seen.append(num)


def main():
    min = int(input("Min: "))
    max = int(input("Max: "))
    nNum = int(input("nNum: "))

    flag = 1
    i = 1
    while (flag == 1):
        try:
            RNG(min, max, nNum, i)
            newFlag = input("Again(Y/N)?")
            newFlag = newFlag.lower()
            if newFlag == 'n':
                flag = 0
        except Error as e:
            print(e)
            break
        i += 1
main()
