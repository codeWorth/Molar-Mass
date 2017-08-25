from molarMass import findMass
from balance import balanceEquation
from balance import isValid
from massToMass import massToMass

print("Programs: ")
print("  1. Molar Mass Calculator")
print("  2. Chemical Equation Balancer")
print("  3. Mass to Mass Converter")
print("Enter q to quit")

while True:
    msg = input("Enter program number, or h for help: ")
    if (msg == "q"):
        continue
    elif (msg == "1"):
        msg = input("Molecular Formula: ")
        result = findMass(msg)
        
        print("Total Mass: " + str(round(result[0], 4)))
        for i, name in enumerate(result[1]):
            print(name + ": Mass: " + str(round(result[2][i], 4)) + ", Percent: " + str(round(result[2][i]/result[0]*100, 4)) + "%")
            
    elif (msg == "2"):
        msg = input("Chemical Equation (use > for arrow): ")
        print(balanceEquation(msg)[0])

    elif (msg == "3"):
        msg = input("Chemical Equation (use > for arrow): ")
        results = massToMass(msg)
        
        print("Mass of each compound: ")
        for i, molecule in enumerate(results[1]):
            print(molecule + ":  Mass:" + str(round(results[0]*results[3][i]*results[2][i], 4)))
        
    
    elif (msg == "h"):
        print("Programs: ")
        print("  1. Molar Mass Calculator")
        print("  2. Chemical Equation Balancer")
        print("  3. Mass to Mass Converter")
        print("Enter q to quit")
    else:
        print("I don't understand that command!")
