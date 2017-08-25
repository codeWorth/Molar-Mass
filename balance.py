import numpy as np
from numpy.linalg import inv
import fractions
from fractions import Fraction

def add(currentAmount, currentElement):
    if (currentElement in elements):
        moleculeAmounts[-1][elements.index(currentElement)] += currentAmount
    else:
        elements.append(currentElement)
        moleculeAmounts[-1].append(currentAmount)
        for molecule in moleculeAmounts[:-1]:
            molecule.append(0)

def process(molecule, mult=1):
    currentElement = ""
    currentAmount = 1
    parens = 0
    inParens = False
    hadParens = False
    for char in molecule:
        if (char == ")"):
            parens -= 1

            if (parens == 0):
                inParens = False
                hadParens = True
            else:
                currentElement += char
        elif (inParens):
            currentElement += char
            if (char == "("):
                parens += 1
        elif (char == "("):
            parens += 1
            if (currentElement != ""):
                if (hadParens):
                    process(currentElement, int(currentAmount) * mult)
                else:
                    add(int(currentAmount) * mult, currentElement)

                hadParens = False
                currentAmount = 1
                currentElement = ""
                
            inParens = True
        elif (char.isdigit()):
            if (currentAmount == 1):
                currentAmount = char
            else:
                currentAmount += char
        elif (char.lower() == char or currentElement == ""):
            currentElement += char
        else:
            if (hadParens):
                process(currentElement, int(currentAmount) * mult)
            else:
                add(int(currentAmount) * mult, currentElement)

            hadParens = False
            parens = 0
            currentAmount = 1
            currentElement = char

    if (hadParens):
        process(currentElement, int(currentAmount) * mult)
    else:
        add(int(currentAmount) * mult, currentElement)
    
while True:
    molecule = input("Expression (use > for arrow): ")
    molecule = "".join(molecule.split())
    if (molecule == "q"):
        break
    
    elements = []
    moleculeAmounts = []

    sides = molecule.split(">")
    reactants = sides[0].split("+")
    products = sides[1].split("+")

    for reactant in reactants:
        moleculeAmounts.append([0]*len(elements))
        process(reactant)

    for product in products:
        moleculeAmounts.append([0]*len(elements))
        process(product)

    molecules = len(moleculeAmounts)
    if (len(elements) < molecules - 1):
        print("I can't solve this!")
        continue;

    reactantsMatrix = np.matrix(moleculeAmounts[:len(reactants)])
    productsMatrix = np.matrix(moleculeAmounts[len(reactants):])
    if (0 in reactantsMatrix.sum(axis=0).tolist()[0]):
        print("Element(s) missing in the reactant(s), can't solve!")
        continue;
    if (0 in productsMatrix.sum(axis=0).tolist()[0]):
        print("Element(s) missing in the product(s), can't solve!")
        continue;

    extraElements = len (moleculeAmounts[0]) - molecules + 1
    if (extraElements > 0):
        for i, molAm in enumerate(moleculeAmounts):
            moleculeAmounts[i] = molAm[:-extraElements]

    constantsMatrix = np.matrix(moleculeAmounts[-1]).transpose()
    reactantsMatrix = np.matrix(moleculeAmounts[:len(reactants)])
    if (len(moleculeAmounts) - len(reactants) - 1 == 0):
        cMatrix = reactantsMatrix
    else:
        productsMatrix = np.matrix(moleculeAmounts[len(reactants):-1]) * -1
        cMatrix = np.vstack((reactantsMatrix, productsMatrix))
    
    cMatrix = inv(cMatrix).transpose()
    answer = np.append(np.dot(cMatrix, constantsMatrix), [[1]], 0)

    rMatrix = np.matrix(moleculeAmounts[:len(reactants)])
    pMatrix = np.matrix(moleculeAmounts[len(reactants):]) * -1

    answer = answer.transpose().tolist()[0]
    
    check = np.vstack((rMatrix, pMatrix)).tolist()
    checkSum = [0]*len(check[0])
    for i, row in enumerate(check):
        for j in range(len(row)):
            row[j] *= answer[i]
            checkSum[j] += row[j]

    if not(all(v == 0 for v in checkSum)):
        print("Not solvable!")
        continue;
    
    for i, num in enumerate(answer):
        frac = Fraction(num).limit_denominator(100)
        answer[i] = (frac.numerator, frac.denominator)

    for i, frac in enumerate(answer):
        mult = frac[1]
        if (mult == 1):
            continue
        
        answer[i] = (frac[0], 1)
        for j, frac1 in enumerate(answer):
            if (j != i):
                answer[j] = (frac1[0]*mult, frac1[1])

    gcd = answer[0][0]
    for num in answer[1:]:
        gcd = fractions.gcd(gcd, num[0])

    for i, tup in enumerate(answer):
        answer[i] = int(tup[0]/gcd)

    solvedExp = ""
    i = 0
    for reactant in reactants:
        if (answer[i] != 1):
            solvedExp += str(answer[i])

        solvedExp += reactant + " + "
        i += 1

    solvedExp = solvedExp[:-3] + " > "

    for product in products:
        if (answer[i] != 1):
            solvedExp += str(answer[i])

        solvedExp += product + " + "
        i += 1

    solvedExp = solvedExp[:-3]          
    print(solvedExp)

