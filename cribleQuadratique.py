#coding utf-8
#!/usr/bin/env python3

import math

def primeNumbers(limit, primeList):
    for i in range(1,limit):
        if isPrime(i, primeList):
            primeList.append(i) 

def isPrime(number, primeList):
    for i in primeList:
        if i != 1 and i != number and number % i == 0:
            return False
    return True

if __name__ == "__main__":
    s = "hello world"
    print(s)
    primeList = []
    primeNumbers(100, primeList)
    for item in primeList:
        print(item)

