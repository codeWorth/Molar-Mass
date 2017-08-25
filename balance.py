import numpy as np
from numpy.linalg import inv
import fractions
from fractions import Fraction
import copy

elements = []
moleculeAmounts = []
coef = []

def isValid(moleculeAmounts, lenReactants, answer):
    rMatrix = np.matrix(moleculeAmounts[:lenReactants])
    pMatrix = np.matrix(moleculeAmounts[lenReactants:]) * -1
    
    check = np.vstack((rMatrix, pMatrix)).tolist()
    checkSum = [0]*len(check[0])
    for i, row in enumerate(check):
        for j in range(len(row)):
            row[j] *= answer[i]
            checkSum[j] += row[j]

    if not(all(v == 0 for v in checkSum)):
        return False
    else:
        return True

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
    began = False
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
            began = True
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
            if not(began):
                if (coef[-1] == 0):
                    coef[-1] = char
                else:
                    coef[-1] += char
            else:                
                if (currentAmount == 1):
                    currentAmount = char
                else:
                    currentAmount += char
        elif (char.lower() == char or currentElement == ""):
            began = True
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

def processEquation(equation):
    global elements, moleculeAmounts, coef
    
    equation = "".join(equation.split())

    coef = []
    elements = []
    moleculeAmounts = []

    sides = equation.split(">")
    reactants = sides[0].split("+")
    products = sides[1].split("+")

    for reactant in reactants:
        moleculeAmounts.append([0]*len(elements))
        coef.append(0)
        process(reactant)

    for product in products:
        moleculeAmounts.append([0]*len(elements))
        coef.append(0)
        process(product)

    coef = [int(x) for x in coef]
    return (elements, moleculeAmounts, reactants, products, coef)

def removeColumn(array, j):
    for row in array:
        del row[j]
    
def balanceEquation(molecule):
    global elements, moleculeAmounts
    result = processEquation(molecule)
    reactants = result[2]
    products = result[3]

    molecules = len(moleculeAmounts)
    if (len(elements) < molecules - 1):
        print("I can't solve this!")
        return ""

    reactantsMatrix = np.matrix(moleculeAmounts[:len(reactants)])
    productsMatrix = np.matrix(moleculeAmounts[len(reactants):])
    if (0 in reactantsMatrix.sum(axis=0).tolist()[0]):
        print("Element(s) missing in the reactant(s), can't solve!")
        return ""
    if (0 in productsMatrix.sum(axis=0).tolist()[0]):
        print("Element(s) missing in the product(s), can't solve!")
        return ""

    tempAmounts = copy.deepcopy(moleculeAmounts) #save copy
    lenReactants = len(reactants)
    
    constantsMatrix = np.matrix(moleculeAmounts[-1]) #shape
    constantsMatrix.fill(0) #fill with 0s
    used = False
    removeIndex = 0
    for i, c in enumerate(coef):
        if (c > 0):
            used = True
            if i < len(reactants): #for each coefficient, if it exists, add the amounts * coefficient
                constantsMatrix = np.add(constantsMatrix, np.matrix(moleculeAmounts[removeIndex]) * c * -1)
                lenReactants -= 1 #this is in the reactants section so a reactant is getting removed
            else:
                constantsMatrix = np.add(constantsMatrix, np.matrix(moleculeAmounts[removeIndex]) * c)
                
            del moleculeAmounts[removeIndex]
        else:
            removeIndex += 1
            

    if not(used): #if we never had a valid coefficient
        constantsMatrix = np.matrix(moleculeAmounts[-1])
        del moleculeAmounts[i]

    constantsList = False
    extraElements = len (moleculeAmounts[0]) - len (moleculeAmounts)
    if (extraElements > 0):
        constantsList = constantsMatrix.tolist()[0]
        for i, moleculeAmount in enumerate(moleculeAmounts): #make moleculeAmounts square
            if (extraElements == 0):
                break

            j = 0
            for amount in moleculeAmount:
                if (amount == 0):
                    removeColumn(moleculeAmounts, j)
                    del constantsList[j]
                    extraElements -= 1
                    if (extraElements == 0):
                        break

                else:
                    j += 1

    if (constantsList):
        constantsMatrix = np.matrix(constantsList)

    if (extraElements > 0):
        constantsList = constantsMatrix.tolist()[0]
        for i, moleculeAmount in enumerate(moleculeAmounts): #finish making moleculeAmounts square
            if (extraElements == 0):
                break
            for j, amount in enumerate(moleculeAmount):
                removeColumn(moleculeAmounts, j)
                del constantsList[j]
                extraElements -= 1
                if (extraElements == 0):
                    break

    if (constantsList):
        constantsMatrix = np.matrix(constantsList)

    reactantsMatrix = np.matrix(moleculeAmounts[:lenReactants])
    if (len(moleculeAmounts) == lenReactants):
        cMatrix = reactantsMatrix
    elif (lenReactants == 0):
        cMatrix = np.matrix(moleculeAmounts[lenReactants:]) * -1
    else:
        productsMatrix = np.matrix(moleculeAmounts[lenReactants:]) * -1
        cMatrix = np.vstack((reactantsMatrix, productsMatrix))
    
    cMatrix = inv(cMatrix).transpose() #invert, solving step 1
    answer = np.dot(cMatrix, constantsMatrix.transpose()).transpose().tolist()[0] #dot product, solving step 2

    for i, c in enumerate(coef): #add known coef to answer
        if (c > 0):
            answer.insert(i, c)
            
    if not(used):
        answer.append(1)

    moleculeAmounts = tempAmounts #revert moleculeAmounts

    if not(isValid(moleculeAmounts, len(reactants), answer)):
        print("Not solvable!")
        return ""
    
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
    return(solvedExp, reactants, products, answer)

