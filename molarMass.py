massesFile = open("massSheet.txt", "r");

names = []
masses = []
symbols = []
atomicNumbers = []

for line in massesFile.read().splitlines():
    words = line.split()
    masses.append(words[0])
    names.append(words[1])
    symbols.append(words[2])
    atomicNumbers.append(words[3])

def add(currentAmount, currentElement, mult):
    realAmount = mult
    if (currentAmount != ""):
        realAmount = int(currentAmount) * int(mult)
    
    if (currentElement in elements):
        amounts[elements.index(currentElement)] += realAmount
    else:
        elements.append(currentElement)
        amounts.append(realAmount)

def process(molecule, mult=""):
    if (mult == ""):
        mult = 1
    
    currentElement = ""
    currentAmount = ""
    inParens = False
    hadParens = False
    for char in molecule:
        if (char == "("):
            if (currentElement != ""):
                if (hadParens):
                    process(currentElement, currentAmount)
                else:
                    add(currentAmount, currentElement, mult)

                hadParens = False
                currentAmount = ""
                currentElement = ""
                
            inParens = True
        elif (char == ")"):
            inParens = False
            hadParens = True
        elif (inParens):
            currentElement += char
        elif (char.isdigit()):
            currentAmount += char
        elif (char.lower() == char or currentElement == ""):
            currentElement += char
        else:
            if (hadParens):
                process(currentElement, currentAmount)
            else:
                add(currentAmount, currentElement, mult)

            hadParens = False
            currentAmount = ""
            currentElement = char

    if (hadParens):
        process(currentElement, currentAmount)
    else:
        add(currentAmount, currentElement, mult)
    
while True:
    molecule = input("Formula: ")
    if (molecule == "q"):
        break
    
    elements = []
    amounts = []
    process(molecule)

    moleculeMasses = []
    moleculeNames = []
    totalMass = 0
    for j, element in enumerate(elements):
        i = symbols.index(element)
        thisAmount = int(amounts[j])
        totalMass += float(masses[i]) * thisAmount
        moleculeMasses.append(float(masses[i]) * thisAmount)
        moleculeNames.append(names[i])

    print("Total Mass: " + str(round(totalMass, 4)))
    for i, name in enumerate(moleculeNames):
        print(name + ": Mass: " + str(round(moleculeMasses[i], 4)) + ", Percent: " + str(round(moleculeMasses[i]/totalMass*100, 4)) + "%")


        
