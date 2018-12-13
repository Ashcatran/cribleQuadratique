#coding utf-8
#!/usr/bin/env python3

#https://www.utc.fr/~wschon/sr06/UtCrible/QuadraSievePage.php
#http://pauillac.inria.fr/~maranget/X/IF/PI/maranget/sujet.html
#https://pdfs.semanticscholar.org/14cb/d2f962f00cd7572e4e45f6c8ea7ce4fbcd81.pdf


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

def gcd(a,b): #euclide's algorithm
    if b == 0:
        return a 
    if a >= b:
        return gcd(b, a % b) 
    return gcd(b, a)

if __name__ == "__main__":
    """
    s = "hello world"
    print(s)
    N = 403034474719 
    B = 241 
    L = 1850
    primeList = []
    primeNumbers(100, primeList)
    for item in primeList:
        print(item)
    """
    print(gcd(56, 6))

