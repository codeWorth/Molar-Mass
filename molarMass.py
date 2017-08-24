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

def add(currentAmount, currentElement):
    if (currentElement in elements):
        amounts[elements.index(currentElement)] += currentAmount
    else:
        elements.append(currentElement)
        amounts.append(currentAmount)

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


        
