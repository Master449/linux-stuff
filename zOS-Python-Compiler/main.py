from datetime import datetime

RX  = {
    # RX Instructions
    "Load"            : "L     ",
    "Add"             : "A     ",
    "Subtract"        : "S     ",
    "Multiply"        : "M     ",
    "Divide"          : "D     ",
    # Other Instructions
    "Store"           : "ST    ",
    "DefineConstant"  : "DC    ",
    "DefineStorage"   : "DS    ",
    "EndProgram"      : "BR    ",
    "Dump"            : "XDUMP ",
    "Print"           : "XPRNT ",
    "Literal"         : "LTORG "
}

RR = {
    # RR Instructions
    "Load"           : "LA    ",
    "Add"            : "AR    ",
    "Subtract"       : "SR    ",
    "Multiply"       : "MR    ",
    "Divide"         : "DR    ",
    "Store"          : "ST    "
}

Register = {
    "Register0"  : "0",
    "Register1"  : "1",
    "Register2"  : "2",
    "Register3"  : "3",
    "Register4"  : "4",
    "Register5"  : "5",
    "Register6"  : "6",
    "Register7"  : "7",
    "Register8"  : "8",
    "Register9"  : "9",
    "Register10" : "10",
    "Register11" : "11",
    "Register12" : "12"
}

today = datetime.now().strftime("%m-%d-%Y")
section = 2
AssignName = "LAB 4"

DocBox = f'''
******************************************************************                          
*                                                                *                          
* CSCI 360-{section}                {AssignName}                    SPRING 2023 *
*                                                                *                          
* PROGRAMMER NAME:                                               *                          
*                                                                *                          
*            DATE: {today}                                    *                          
*                                                                *                          
*    PROGRAM NAME:                                               *                          
*                                                                *                          
*        FUNCTION:                                               *                          
*                                                                *                          
*           NOTES:                                               *                          
*                                                                *                          
****************************************************************** 
*
'''
def Spacer(label, n):
    length = len(label)
    if length == 0:
        return "         "
    else:
        for x in range(length, n):
            label += " "
    return label

# String to hold the entire program
Program = DocBox + "MAIN     CSECT\n         USING MAIN,15\n"

with open('input.txt', 'r') as file:
    for line in file:
        if line.startswith("#"):
            continue

        if line.startswith("*"):
            Program += line
            continue

        newline = line.split(" ")
        
        for i in range(len(newline)):
            newline[i] = newline[i].strip('\n')

        try:
            Label, Operation, Arg1, Arg2, *rest = newline
        except:
            try:
                Label, Operation, Arg1, *rest = newline
            except:
                try:
                    Label, Operation = newline
                    rest = ""
                except:
                    print("Achievement: How did we get here?")

        if Operation == "Literal":
            Program += Spacer("", 9) + RX["Literal"] + "\n"
            continue

        if (Label in RR) or (Label in RX):
            Program += Spacer(Label, 9)
        else:
            Program += Spacer("", 9)
        
        if Arg1 in Register and Arg2 in Register:
            Program += RR[Operation] + Register[Arg1] + "," + Register[Arg2]
        elif Arg1 in Register:
            try:
                Program += RR[Operation] + Register[Arg1] + "," + Arg2
            except:
                pass
        else:
            Program += RX[Operation] + Arg1
            
        for x in rest:
            Program += rest[x]
                

        Program += "\n"

Program += "         END   MAIN\n"

print(Program)
