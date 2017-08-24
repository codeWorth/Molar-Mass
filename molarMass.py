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
    realAmount = 1
    if (currentAmount != ""):
        realAmount = int(currentAmount)
    
    if (currentElement in elements):
        amounts[elements.index(currentElement)] += realAmount
    else:
        elements.append(currentElement)
        amounts.append(realAmount)
    
while True:
    molecule = input("Formula: ")
    if (molecule == "q"):
        break
    
    elements = []
    amounts = []
    currentElement = molecule[0]
    currentAmount = ""
    for char in molecule[1:]:
        if (char.isdigit()):
            currentAmount += char
        elif (char.lower() == char):
            currentElement += char
        else:
            add(currentAmount, currentElement)

            currentAmount = ""
            currentElement = char

    add(currentAmount, currentElement)

    moleculeMasses = []
    moleculeNames = []
    totalMass = 0
    for element in elements:
        i = symbols.index(element)
        totalMass += float(masses[i])
        moleculeMasses.append(float(masses[i]))
        moleculeNames.append(names[i])

    print("Total Mass: " + str(totalMass))
    for i, name in enumerate(moleculeNames):
        print(name + ": Mass: " + str(moleculeMasses[i]) + ", Percent: " + str(round(moleculeMasses[i]/totalMass*100, 3)) + "%")


        
