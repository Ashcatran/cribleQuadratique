#coding utf-8
#!/usr/bin/env python3

import math

def primeNumbers(limit, primeList):
    for i in range(1,limit):
        print(i, isPrime(i, primeList))

def isPrime(number, primeList):
    for i in range(2, math.floor(math.sqrt(number))+1):
        #print (number, i)
        if number % i == 0:
            return False
    primeList.append(number)
    return True

if __name__ == "__main__":
    s = "hello world"
    print(s)
    primeList = []
    primeNumbers(10, primeList)
    for item in primeList:
        print(item)

