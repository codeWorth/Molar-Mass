from molarMass import findMass
from balance import balanceEquation
from balance import isValid
from balance import processEquation

def massToMass(equation):        
    results = processEquation(equation)
    elements = results[0]
    moleculeAmounts = results[1]
    reactants = results[2]
    products = results[3]
    coef = results[4]
    adjustedCoef = [(1 if x == 0 else x) for x in coef]

    if not(isValid(moleculeAmounts, len(reactants), adjustedCoef)):
        results = balanceEquation(equation)
        coef = results[3]

    masses = []
    names = []
    print("These are your compounds: ")
    for i, molecule in enumerate(reactants+products):
        results = findMass(molecule)
        masses.append(results[0])
        names.append(results[3])
        print("  " + str(i + 1) + ": " + results[3])

    compNum = int(input("Which compound do you know the mass of: ")) - 1
    massKnown = float(input("Enter its mass: "))

    moles = massKnown/masses[compNum]/coef[compNum]

    return (moles, names, masses, coef)

    
    


