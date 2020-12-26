#Deductive FS
#Jae W Hwang
import time
def AssignFaults(a):
    TempFaults = dict(Faults)
    Tempin1list = list()
    Tempin2list = list()
    TempFaults["Node"] = a["In1Node"]
    TempFaults["SA"] = 0
    Tempin1list.append(dict(TempFaults))
    TempFaults["Node"] = a["In1Node"]
    TempFaults["SA"] = 1
    Tempin1list.append(dict(TempFaults))
    a["In1Faults"] = list(Tempin1list)
    if not a["GateType"] == "INV":
        if not a["GateType"] == "BUF":
            TempFaults["Node"] = a["In2Node"]
            TempFaults["SA"] = 0
            Tempin2list.append(dict(TempFaults))
            TempFaults["Node"] = a["In2Node"]
            TempFaults["SA"] = 1
            Tempin2list.append(dict(TempFaults))
            a["In2Faults"] = list(Tempin2list)




#Gate: Gate Number,Exec In1 Node, In1 Value, In1 Faults, In2 Node, In2 Value, In2 Faults, Out Node, Out Value, Faults
Faults = {
"Node" : -1,
"SA" : -1
}

Gate = {
"Num" : -1,
"GateType" : None,
"Exec": 0,
"In1Node" : -1,
"In1Val" : -1,
"In1Faults" : list(),
"In2Node" : -1,
"In2Val" : -1,
"In2Faults" : list(),
"OutNode" : -1,
"OutVal" : -1,
"OutFaults" : list()
}



TempFaults = dict()
TempGate = dict()
Gates = list()
Inputs = list()
Outputs = list()

print("Deductive Fault Simulator(Deductive-FS)")
print("This program will perform deductive fault simulation on all nodes of the circuit")
print("By performing Deductive fault simulation, user can determine which stuck-at faults can be detected when a certain inputs are applied\n")
filename = input("Please enter the name of the circuit file you would like to simulate (Ex.s27.txt):")
f = open(filename)
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
#from termcolor import colored, cprint
#cprint('\nCalling Circuit Info', 'blue', attrs=['blink'])
print("Calling Circuit Info")
#time.sleep(3)
templist = list()
Gatenum = -1

#Initialize Gates
for elements in f:
    TempGate = dict(Gate)
    elements.rstrip()
    print(elements.rstrip())
    if not elements.startswith("INPUT"):
        if not elements.startswith("OUTPUT"):
            Gatenum = Gatenum + 1
            TempGate["Num"] = Gatenum
            templist = elements.rstrip().split()
            if not elements.startswith("BUF"):
                if not elements.startswith("INV"):
                    TempGate["GateType"] = templist[0]
                    TempGate["In1Node"] = templist[1]
                    TempGate["In2Node"] = templist[2]
                    TempGate["OutNode"] = templist[3]
                    #print(Gate)
                    #continue
            if elements.startswith("BUF") or elements.startswith("INV"):
                TempGate["GateType"] = templist[0]
                TempGate["In1Node"] = templist[1]
                TempGate["OutNode"] = templist[2]
                #print(Gate)
            Gates.append(dict(TempGate))

    if elements.startswith("INPUT"):
        templist = elements.rstrip().split()
        for elements in templist[1:len(templist)-1]:
            Inputs.append({"Node": elements, "Value": -1})

print(Inputs)
print(len(Inputs))
#for elements in Gates:
#    print(elements)


print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

#Assign Faults
for elements in Gates:
    AssignFaults(elements)

#Taking Input Vector from user
Inputcorrect = True
print("Please enter the input vector you would like to simulate[", len(Inputs), "Digit Binary Number]:", end="")
Userinput = input()
if len(Userinput) != len(Inputs):
    Inputcorrect = False

for elements in Userinput:
    if elements != '0':
        if elements != '1':
            Inputcorrect = False

while(Inputcorrect == False):
    Inputcorrect = True
    print("Please enter the correct input vector[", len(Inputs), "Digit Binary Number]:", end="")
    Userinput = input()
    if len(Userinput) != len(Inputs):
        Inputcorrect = False

    for elements in Userinput:
        if elements != '0':
            if elements != '1':
                Inputcorrect = False

for i in range(len(Userinput)):
    Inputs[i]["Value"] = Userinput[i]

#Initial value assignment based on user's input
for elements in Gates:
    for elements2 in Inputs:
        if elements["In1Node"] == elements2["Node"]:
            elements["In1Val"] = elements2["Value"]

        if elements["In2Node"] == elements2["Node"]:
            elements["In2Val"] = elements2["Value"]

#Ready_Gates Initialize
Ready_Gates = list()

for elements in Gates:
    if elements["GateType"] == "INV" or elements["GateType"] == "BUF":
        if elements["Exec"] == 0:
            if elements["In1Val"] != -1:
                Ready_Gates.append(elements["Num"])
    else:
        if elements["In1Val"] != -1:
            if elements["In2Val"] != -1:
                if elements["Exec"] == 0:
                    Ready_Gates.append(elements["Num"])

for elements in Ready_Gates:
    print(elements)

#Ready Gate Executions
Flagdetector = list()
count = 0
while Ready_Gates:
    for elements in Ready_Gates:
        for elements2 in Gates:
            if elements == elements2["Num"]:
                elements2["Exec"] = 1
                if elements2["In1Val"] == '0':
                    count = 0
                    for elements3 in elements2["In1Faults"]:
                        if elements2["In1Node"] == elements3["Node"]:
                            if elements3["SA"] == 0:
                                Flagdetector.append(count)
                        count = count + 1

                if elements2["In1Val"] == '1':
                    count = 0
                    for elements3 in elements2["In1Faults"]:
                        if elements2["In1Node"] == elements3["Node"]:
                            if elements3["SA"] == 1:
                                Flagdetector.append(count)
                        count = count + 1


                for elements3 in Flagdetector:
                    del elements2["In1Faults"][elements3]

                Flagdetector.clear()

                if elements2["In2Val"] == '0':
                    count = 0
                    for elements3 in elements2["In2Faults"]:
                        if elements2["In2Node"] == elements3["Node"]:
                            if elements3["SA"] == 0:
                                Flagdetector.append(count)
                        count = count + 1

                if elements2["In2Val"] == '1':
                    count = 0
                    for elements3 in elements2["In2Faults"]:
                        if elements2["In2Node"] == elements3["Node"]:
                            if elements3["SA"] == 1:
                                Flagdetector.append(count)
                        count = count + 1


                for elements3 in Flagdetector:
                    del elements2["In2Faults"][elements3]

                Flagdetector.clear()

                if elements2["GateType"] == "INV":
                    if int(elements2["In1Val"]) == 0:
                        elements2["OutVal"] = 1
                    if int(elements2["In1Val"]) == 1:
                        elements2["OutVal"] = 0
                    for elements3 in elements2["In1Faults"]:
                        elements2["OutFaults"].append(elements3)

                if elements2["GateType"] == "BUF":
                    if int(elements2["In1Val"]) == 0:
                        elements2["OutVal"] = 0
                    if int(elements2["In1Val"]) == 1:
                        elements2["OutVal"] = 1
                    for elements3 in elements2["In1Faults"]:
                        elements2["OutFaults"].append(elements3)

                if elements2["GateType"] == "OR":
                    if (int(elements2["In1Val"]) + int(elements2["In2Val"])) >= 1:
                        elements2["OutVal"] = 1

                    #For input1 = 0; Input2 = 0
                    if int(elements["In1Val"]) == 0:
                        if int(elements["In2Val"]) == 0:
                            templist = list()
                            tempcount = 0
                            for elements3 in elements2["In1Faults"]:
                                for elements4 in elements2["In2Faults"]:
                                    if elements4["Node"] == elements3["Node"]:
                                        if elements4["SA"] == elements3["SA"]:
                                            templist.append(tempcount)
                                    tempcount = tempcount + 1
                            for d in templist:
                                elements2["In2Faults"].remove(d)
                            templist.clear()

                            for elements3 in elements2["In1Faults"]:
                                elements2["OutFaults"].append(elements3)

                            for elements4 in elements2["In2Faults"]:
                                elements2["OutFaults"].append(elements4)

                    #For Input1 = 0; Input2 = 1
                    if int(elements["In1Val"]) == 0:
                        if int(elements["In2Val"]) == 1:
                            templist = list()
                            templist2 = list()
                            tempcount = 0
                            tempcount2 = 0
                            for elements3 in elements2["In1Faults"]:
                                for elements4 in elements2["In2Faults"]:
                                    if elements4["Node"] == elements3["Node"]:
                                        if elements4["SA"] == elements3["SA"]:
                                            templist.append(tempcount)
                                            templist2.append(tempcount2)
                                    tempcount = tempcount + 1
                                Tempcount2 = tempcount2 + 1
                            for d in templist:
                                elements2["In2Faults"].remove(d)
                            for e in templist2:
                                elements2["In1Faults"].remove(e)
                            templist.clear()
                            templist2.clear()

                            for elements3 in elements2["In1Faults"]:
                                elements2["OutFaults"].append(elements3)

                            for elements4 in elements2["In2Faults"]:
                                elements2["OutFaults"].append(elements4)




                    if int(elements["In1Val"]) == 1:
                        if int(elements["In2Val"]) == 0:
                            print()

                    if int(elements["In1Val"]) == 1:
                        if int(elements["In2Val"]) == 1:
                            print()



                if elements2["GateType"] == "NOR":
                    if (int(elements2["In1Val"]) + int(elements2["In2Val"])) >= 1:
                        elements2["OutVal"] = 0








    Ready_Gates.clear()



                #if elements2["GateType"] == "INV" or elements2["GateType"] == BUF:
                #    elements2["OutVal"] =



for elements in Gates:
    print(elements)


print(Inputs)
