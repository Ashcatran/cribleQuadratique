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
    for i in range(1,limit):
        if isPrime(i, primeList):
            primeList.append(i)

def getPrimeNumbers(start, end, primeList):
    number = end - start
    prevStatus = 0
    for i in range(start,end):
        if isPrime(i, primeList):
            primeList.append(i)
           #print("found new prime:", i)
        status = (i - start)*100 // number
        if status != prevStatus:
            print(status, "%")

def isPrime(number, primeList):
    for i in primeList:
        if i != 1 and i != number and number % i == 0:
            return False
    return True

def getPrimeNumbersUpTo(limit):
    lastPrime = 2
    primeList = []
    try:
        primeList = pickle.load(open("primeList.p", "rb"))
        lastPrime = primeList[-1]
    except FileNotFoundError :
    #as identifier:
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
    if b == 0:
        return a 
    if a >= b:
        return gcd(b, a % b) 
    return gcd(b, a)

def factorBaseSize(N):
    F = pow(math.exp(math.sqrt(math.log(N)*math.log(math.log(N)))),math.sqrt(2)/4)
    F = int(math.ceil(F))
    return F

def primeFactorization(N, primeList):
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
    if number < 0:
        return False
    sqrt = math.sqrt(number)
    floorSqrt = math.floor(math.sqrt(number))
    return True if sqrt == floorSqrt else False

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def completelyFactores(q, S, e):
    n = 1
    for i in range(len(S)):
        n = n*(S[i]**e[i])
    return n == q

def showMatrix(m):
    for row in m:
        print(row)

def makeBinaryVectors(matrix):
    newMatrix = []
    for row in matrix:
        newRow = []
        for element in row:
            newRow.append(element % 2)
        newMatrix.append(newRow)
    return newMatrix

def findLinearCombination(matrix, allCombinations):
    combination =[0 for i in range(len(matrix))]
   # result = [0 for i in range(len(matrix[0]))]
    valid = False
    while valid == False:
       # print(len(allCombinations))
   #     combination =[0 for i in range(len(matrix))]
        result = [0 for i in range(len(matrix[0]))]
        combination = allCombinations[0]
    # print("combination", combination)

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result[j] = result[j] + matrix[i][j]*combination[i]
        valid = True
        for i in range(len(result)):
            result[i] = result[i]%2
            if result[i] != 0:
                valid = False
        if valid == False:
            #allCombinations.remove(combination)
            removeCombination(allCombinations, combination)
   # print("matrix")
    #print(matrix)
   # print("combination", combination)
   # print("result", result)


    return combination

def removeCombination(allCombinations, combination):
    allCombinations.remove(combination)
    if len(allCombinations) == 0:
        print("Tested all combination, none worked :(")
        exit()

if __name__ == "__main__":
    """
    s = "hello world"
    print(s)
    """
    #N = 403034474719 
    #B = 241 
    #L = 1850
    #N = 24961 
    #N = 1511*1523
    #N = 227*229
    #N = 3119*3121
    N = 2301351
    limit = N
    #print(limit)
    primeList = getPrimeNumbersUpTo(limit)
    print("loaded", len(primeList), "prime numbers, from", primeList[0], "to", primeList[-1])
    if isPrime(N, primeList):
        print(N, "is prime")
        exit(0)
    m = math.floor(math.sqrt(N))
    #print("m", m)
    f = factorBaseSize(N)
    print("vector base size", f)
    #primeList = primeList[0:f]
    #print("primeList", primeList)
    #facto = primeFactorization(N, primeList)
    #print(facto)
    #for p in primeList:
    #    if facto[primeList.index(p)] != 0:
    #       print(p, facto[primeList.index(p)])
    # Création de la base de facteurs
    S = [-1]
    for p in primeList:
        if legendre(N, p) == 1:
            S.append(p)
        if len(S) == f:
            break;
            
    #print("S", S)
    matrix = []
    aVector = []
    bVector = []
    for x in range(-f,f+1):
        #print(i)
        q = (x + m)**2 - N
        a = x + m
        e = primeFactorization(q, S[1:])
        cf = completelyFactores(q, S, e)
        if cf:
           # print(x, a, q, e, cf)
            aVector.append(a)
            bVector.append(q)
            matrix.append(e)
    #print("ax", aVector)
    #print("bx", bVector)
    #showMatrix(matrix)
    binaryMatrix = makeBinaryVectors(matrix)
    #showMatrix(binaryMatrix)
    allCombinations = list(itertools.product([0, 1], repeat = len(matrix)))
    #allCombinations= [(1,0,1,0,0,0,1)]
    solved = False
    while solved == False:
       # print(len(allCombinations))
        linearCombination = findLinearCombination(binaryMatrix, allCombinations)
        #linearCombination   
        v = [0 for i in range(f)]
        for i in range(len(matrix)):
            for j in range(f):
                v[j] = v[j] + matrix[i][j]*linearCombination[i]
        for i in range(len(v)):
            v[i]=v[i]//2
        v[0]=0
        X=1
        for i in range(f):
            X = X*S[i]**v[i]
        X = X%N
        Z = 0
        K=2
        #while not isSquare(Z) or Z == 0:
        while (X**2)%N !=(Z**2)%N: # or K < 1:
            Z = (X - K*X)%N
            K = K+1
           #print(K, Z)
        #X = int(math.sqrt(Z))


    # X = 13922
        #print("X", X)
        Y = 1
        for i in range(len(matrix)):
            if linearCombination[i] > 0:
                Y = Y*aVector[i]*linearCombination[i]
        Y = Y%N
        #print("Y", Y)

        sol1 = gcd(abs(X-Y), N)
        sol2 = gcd(X+Y, N)
        #print("sol1", sol1)
        #print("sol2", sol2)
        #print(X,Y,sol1,sol2)
        if sol1 != 1 and sol2 != 1:
            solved = True
        else:
            #allCombinations.remove(linearCombination)
            removeCombination(allCombinations,linearCombination)
    print("SOLVED!", N , "=", sol1, "*", sol2)
    

