#coding utf-8
#!/usr/bin/env python3

#https://www.utc.fr/~wschon/sr06/UtCrible/QuadraSievePage.php
#http://pauillac.inria.fr/~maranget/X/IF/PI/maranget/sujet.html
#https://pdfs.semanticscholar.org/14cb/d2f962f00cd7572e4e45f6c8ea7ce4fbcd81.pdf


import math
import pickle
import random
import itertools


def primeNumbers(limit, primeList):
    """returns primelist with all prime numbers from 2 to limit"""
    for i in range(1,limit):
        if isPrime(i, primeList):
            primeList.append(i)

def getPrimeNumbers(start, end, primeList):
    """adds all prime numbers between start and end into primelist"""
    number = end - start
    prevStatus = 0
    for i in range(start,end):
        if isPrime(i, primeList):
            primeList.append(i)
        status = (i - start)*100 // number
        if status != prevStatus:
            print(status, "%")

def isPrime(number, primeList):
    """returns true is number is prime"""
    for i in primeList:
        if i != 1 and i != number and number % i == 0:
            return False
    return True

def getPrimeNumbersUpTo(limit):
    """returns a list of all prime numbers from 2 to limit. Loads and saves them from/into a file"""
    lastPrime = 2
    primeList = []
    try:
        primeList = pickle.load(open("primeList.p", "rb"))
        lastPrime = primeList[-1]
    except FileNotFoundError :
        print("Creating new prime list")
    
    if lastPrime < limit:
        print('calculating new primes, from', lastPrime, "to", limit)
        getPrimeNumbers(lastPrime, limit, primeList)
        pickle.dump(primeList, open("primeList.p", 'wb'))
    else:
        old = primeList
        primeList = [p for p in old if p <= limit]
    return primeList
        



def gcd(a,b): #euclide's algorithm
    """return the greatest common divisor of a and b"""
    if b == 0:
        return a 
    if a >= b:
        return gcd(b, a % b) 
    return gcd(b, a)

def factorBaseSize(N):
    """returns the optimal size of the factor base, knowing N"""
    F = pow(math.exp(math.sqrt(math.log(N)*math.log(math.log(N)))),math.sqrt(2)/4)
    F = int(math.ceil(F))
    return F

def primeFactorization(N, primeList):
    """returns the list of factors of N in primelist"""
    i=0
    facto = []
    if N < 0:
        N = -N
        facto.append(1)
    else:
        facto.append(0)
    for p in primeList:
        while N % p**i == 0:
            i = i+1     
        facto.append(i-1)
        i=0
    return facto

def isSquare(number):
    """returns True if number is a perfect square"""
    if number < 0:
        return False
    sqrt = math.sqrt(number)
    floorSqrt = math.floor(math.sqrt(number))
    return True if sqrt == floorSqrt else False

def legendre(a, p):
    """returns the legendre symbol of a and p"""
    return pow(a, (p - 1) // 2, p)

def completelyFactores(q, S, e):
    """returns True if q is completely factored by factors in S to the exponents in e"""
    n = 1
    for i in range(len(S)):
        n = n*(S[i]**e[i])
    return n == q

def showMatrix(m):
    """prints a matrix in a readable format"""
    for row in m:
        print(row)

def makeBinaryVectors(matrix):
    """returns a binary matrix"""
    newMatrix = []
    for row in matrix:
        newRow = []
        for element in row:
            newRow.append(element % 2)
        newMatrix.append(newRow)
    return newMatrix

def findLinearCombination(matrix, allCombinations):
    """finds a linear combination of rows in matrix, using combinations in allCombinations"""
    combination =[0 for i in range(len(matrix))]#indispensable?
    valid = False
    while valid == False:
        result = [0 for i in range(len(matrix[0]))]
        combination = allCombinations[0]

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result[j] = result[j] + matrix[i][j]*combination[i]
        valid = True
        for i in range(len(result)):
            result[i] = result[i]%2
            if result[i] != 0:
                valid = False
        if valid == False:
            removeCombination(allCombinations, combination)
    return combination

def removeCombination(allCombinations, combination):
    """removes combination form allCombinations"""
    allCombinations.remove(combination)
    if len(allCombinations) == 0:
        print("Tested all combination, none worked :(")
        exit()

# looking for X**2 = X**2 mod N
if __name__ == "__main__":
    #N = 403034474719 
    #B = 241 
    #L = 1850
    #N = 24961 
    #N = 1511*1523
    N = 227*229
    #N = 3119*3121
    #N = 2301351 # Doesn't work :(
    limit = N
    primeList = getPrimeNumbersUpTo(limit)
    print("loaded", len(primeList), "prime numbers, from", primeList[0], "to", primeList[-1])

    """If N is prime, exit"""
    if isPrime(N, primeList):
        print(N, "is prime")
        exit(0)
    
    m = math.floor(math.sqrt(N))
    f = factorBaseSize(N)
    # Création de la base de facteurs
    S = [-1]
    for p in primeList:
        if legendre(N, p) == 1: # if p is a quadratic residue of N
            S.append(p)
        if len(S) == f:
            break
    
    # calculating vectors and marix
    matrix = []
    aVector = []
    bVector = []
    for x in range(-f,f+1):
        q = (x + m)**2 - N
        a = x + m
        e = primeFactorization(q, S[1:])#ignore -1 in S
        cf = completelyFactores(q, S, e)
        if cf: # if q is S-smooth
            aVector.append(a)
            bVector.append(q)
            matrix.append(e)
    
    # constructing matrix
    binaryMatrix = makeBinaryVectors(matrix)

    # creating all possible combinations
    allCombinations = list(itertools.product([0, 1], repeat = len(matrix)))

    # solving loop
    solved = False
    while solved == False:
        # obtain a valid combination of rows in matrix
        linearCombination = findLinearCombination(binaryMatrix, allCombinations)
        # calculate X
        v = [0 for i in range(f)]
        for i in range(len(matrix)):
            for j in range(f):
                # fectch exponents
                v[j] = v[j] + matrix[i][j]*linearCombination[i]
        for i in range(len(v)):
            v[i]=v[i]//2 # X is a perfect square
        v[0]=0
        X=1
        for i in range(f):
            X = X*S[i]**v[i]
        X = X%N

        # calculate Y
        Y = 1
        for i in range(len(matrix)):
            if linearCombination[i] > 0:
                Y = Y*aVector[i]*linearCombination[i]
        Y = Y%N

        # computing the two factors of N
        sol1 = gcd(abs(X-Y), N)
        sol2 = gcd(X+Y, N)
        if sol1 != 1 and sol2 != 1:
            solved = True
        else:
            removeCombination(allCombinations,linearCombination)
    print("SOLVED!", N , "=", sol1, "*", sol2)
    

