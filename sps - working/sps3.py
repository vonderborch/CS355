#!/usr/bin/python3
import re
import sys
import types

######## Global Variables
# Stacks
dictionary = [] # Stack containing any/all dictionaries, with one created at initial runtime.
execution = [] # Stack containing current location in SPS code
operand = [] # Stack containing any/all operands

# Sept 21, 2011 -- fixed the handling of }{ -- each brace should be a separate token
# A regular expression that matches postscript each different kind of postscript token
pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'

######## Debug Functions
# Debug: Takes a string, outputs error message, current stacks, and then exits program.
def Debug(*s):
    print(s)
    print("REMAINING OPERAND STACK:")
    for i in operand:
        print (i)
    print("REMAINING DICTIONARY STACK:")
    for i in dictionary:
        print (i)
    print("REMAINING EXECUTION STACK:")
    for i in execution:
        print (i)
    sys.exit(1)
    return


######## Common Functions
#### Is Variable
# isNumber: checks if variable (x) is a number and returns result
def isNumber(x):
    if type(x) == int or type(x) == float:
        return True
    return False

# isBool: checks if variable (x) is a bool and returns result
def isBool(x):
    if type(x) == bool:
        return True
    return False

# isString: checks if variable (x) is a string and returns result
def isString(x):
    if type(x) == str:
        return True
    return False
    
# isDict: checks if variable (x) is a dict and returns result
def isDict(x):
    if type(x) is dict == False:
        return False
    return True

#### Convert Variable
# Converts a variable (x) to a number or bool if possible, otherwise returns variable as is
def convert(x):
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            if x == 'true':
                return True
            elif x == 'false':
                return False
            else:
                return x
    
#### Pop Operands
# Pops a number from the list (L) and makes sure its a valid type. If not valid, gives error message (v,s)
def PopNumber(L,s,v):
    x = ListPop(L)
    if isNumber(x) == False:
        Debug("%s in operation %s is not a number or doesn't exist!",v,s)
    return x;
# Pops a boolean from the list (L) and makes sure its a valid type. If not valid, gives error message (v,s)
def PopBoolean(L,s,v):
    x = ListPop(L)
    if isBool(x) == False:
        Debug("%s in operation %s is not a boolean or doesn't exist!",v,s)
    return x;
# Pops two numbers from the list (L) for function s
def PopTwoNumbers(L,s):
    return (PopNumber(L,s,"x1"),PopNumber(L,s,"x2"));
# Pops two booleans from the list (L) for function s
def PopTwoBooleans(L,s):
    return (PopBoolean(L,s,"x1"),PopBoolean(L,s,"x2"));


######## SPS Functions
#### Number Operators
#adds x1 and x2 from the operand stack and puts the result on the operand stack
def _ADD():
    x1,x2 = PopTwoNumbers(operand,"_ADD")
    return ListPush(operand,x1 + x2)

#subtracts x1 and x2 from the operand stack and puts the result on the operand stack
def _SUB():
    x1,x2 = PopTwoNumbers(operand,"_SUB")
    return ListPush(operand,x1 - x2)

#multiplies x1 and x2 from the operand stack and puts the result on the operand stack
def _MUL():
    x1,x2 = PopTwoNumbers(operand,"_MUL")
    return ListPush(operand,x1 * x2)

#divides x1 and x2 from the operand stack and puts the result on the operand stack
def _DIV():
    x1,x2 = PopTwoNumbers(operand,"_DIV")
    return ListPush(L,x1 / x2)

#### Logic Operators
# determines if x1 == x2 and puts the result on the operand stack
def _EQ():
    x1,x2 = PopTwoNumbers(operand,"_EQ")
    t = False
    if x1 == x2:
        t = True
    return ListPush(operand,t)

# determines if x1 < x2 and puts the result on the operand stack
def _LT():
    x1,x2 = PopTwoNumbers(operand,"_LT")
    t = False
    if x1 < x2:
        t = True
    return ListPush(operand,t)

# determines if x1 > x2 and puts the result on the operand stack
def _GT():
    x1,x2 = PopTwoNumbers(operand,"_GT")
    t = False
    if x1 > x2:
        t = True
    return ListPush(operand,t)

#### Boolean Operators
# determines if x1 and x2 have the same truth value and puts the result on the operand stack
def _AND():
    x1,x2 = PopTwoBooleans(operand,"_AND")
    t = False
    if x1 == True and x2 == True:
        t = True
    return ListPush(operand,t)

# determines if x1 or x2 have the same truth value and puts the result on the operand stack
def _OR():
    x1,x2 = PopTwoBooleans(operand,"_OR")
    t = False
    if x1 == True or x2 == True:
        t = True
    return ListPush(operand,t)

# determines if not x1 and puts the result on the operand stack
def _NOT():
    x = PopBoolean(operand,"_OR","x")
    t = True
    if x == True:
        t = False
    return ListPush(operand,t)

#### Stack Operators
# Duplicates the top value on the operand stack
def _DUP():
    t = ListPop(L)
    ListPush(L,t)
    ListPush(L,t)
    return True

# Exchanges the top two values on the operand stack
def _EXCH():
    t = ListPop(L)
    ListPushPosition(L,t, len(operand) - 1)
    return True

# Pops the top value from the operand stack
def _POP():
    return ListPop(L)

# Gets the value of x from a dictionary stack and gets it
# x = key to find result for
def _GET(x):
    temp = []
    found = False
    for i in dictionary:
        if x in i.keys():
            try:
                temp = i[x].copy()
            except:
                temp = i[x]
            found = True
            print(temp)

    if found == True:
        if len(temp) > 1:
            InterpretorLoop(temp)
        else:
            z = convert(temp[0])
            if isNumber(z) == True or isBool(z) == True:
                ListPush(operand, z)
            else:
                _GET(temp[0])
        

    return True

#### Dictionary Creation
# Creates an empty dictionary on the operand stack
def _DICTZ():
    ListPush(operand,{})
    return True

#### DICTIONARY MANIPULATION
# Gets the top value from the operand stack and, if its a dictionary, pushes it to the dictionary stack
def _BEGIN():
    t = ListPop(operand)
    if isDict(t) == False:
        Debug("No Dictionary on the Stack for _BEGIN!")
        return False
    ListPush(dictionary,t)
    return True

# Pops the top dictionary from the dictionary stack
def _END():
    return ListPop(dictionary)

#### Name Defination
# defines a name. creates a new definition if key doesn't exist in top dict, otherwise modifies key
def _DEF(x,L):
    tL = []
    t2 = ''
    t1 = x[1:]
    if isString(t1) == False:
        Debug("T1 in operation _DEF is not a string!")

    temp = ListPopFirst(L)
    if temp != '{':
        t2 = temp
    else:
        curly = 1
        while curly > 0:
            x = ListPopFirst(L)
            tL.append(x)
            if x == '{':
                curly = curly + 1
            elif x == '}':
                curly = curly - 1
        ListPop(tL)
    temp = ListPopFirst(L)
    if temp != 'def':
        Debug("No def to end _DEF command!")

    if t2 != '':
        DictionaryPushItem(t1,t2)
    else:
        DictionaryPushItem(t1,tL)
    return True

#### Stack Printing
# Prints everything on a stack
def _STACK(L):
    for i in L:
        print(i)
    return True

# Pops and prints the top value on a stack
def _EQUALS(L):
    t = ListPop(L)
    print(t)
    return True

######## Stack Control
# Push a dictionary item onto the list
def ListPushItem(L,t,v):
    x = {t:value}
    L[len(dictionary)].append(x)
    return True

# Push an item to the top of the list
def ListPush(L,t):
    L.append(t)
    return True

# Pop an item from the top of the list and return it
def ListPop(L):
    if len(L) == 0:
        Debug("No item on the Selected Stack to pop!")
    return L.pop()

# Pop an item from the bottom of the list and return it
def ListPopFirst(L):
    if len(L) == 0:
        Debug("No item on the Selected Stack to pop!")
    return L.pop(0)

# Push an item to the location desired on the list
def ListPushPosition(L,t,p):
    L.insert(p,t)
    return t

# Push an item to the top dictionary, modifying if key exists, otherwise creating new entry
def DictionaryPushItem(x1,x2):
    t = len(dictionary) - 1
    x = dictionary[t].get(x1,x2)
    if x == None:
        dictionary[t][x1] = dictionary[t].get(x1,x2)
    else:
        dictionary[t][x1] = x2
    return True

######## File Reader
# Given a string, return the tokens it contains
def parse(s):
   tokens = re.findall(pattern, s)
   return tokens

# Given an open file, return the tokens it contains
def parseFile(f):
   tokens = parse(''.join(f.readlines()))
   return tokens

######## Printing
# Prints the output of the program
def printOutput():
    print("")
    print("OPERAND STACK:")
    _STACK(operand)
    print("")
    print("---------------------------------------------")
    print("")
    print("DICTIONARY STACK:")
    for i in dictionary:
        print(i)
        print("=======================")
    return

######## Interpretor
# Main Access for the base interpretor
# L = list to make the execution stack from.
def InterpretorMain(L):
    for word in L:
        ListPush(execution,word)
    _DICTZ()
    _BEGIN()
    InterpretorLoop(execution)

# Interpretor loop: cycles all commands in the passed list
# ex: list to take execution input from
def InterpretorLoop(ex):
    t = ListPopFirst(ex)
    temp = False
    loopRunning = True
    while loopRunning == True:
        z = convert(t)
        if isNumber(z) or isBool(z):
            ListPush(operand,z)
        elif t == 'add':
            _ADD()
        elif t == 'sub':
            _SUB()
        elif t == 'mul':
            _MUL()
        elif t == 'div':
            _DIV()
        elif t == 'eq':
            _EQ()
            LogicLoop(ex)
        elif t == 'lt':
            _LT()
            LogicLoop(ex)
        elif t == 'gt':
            _GT()
            LogicLoop(ex)
        elif t == 'and':
            _AND()
        elif t == 'or':
            _OR()
        elif t == 'not':
            _NOT()
        elif t == 'dup':
            _DUP()
        elif t == 'exch':
            _EXCH()
        elif t == 'pop':
            _POP()
        elif t == 'dictz':
            _DICTZ()
        elif t == 'begin':
            _BEGIN()
        elif t == 'end':
            _END()
        elif t[0] == '/':
            _DEF(t,ex)
        elif t == 'stack':
            _STACK(op)
        elif t == '=':
            _EQUALS(op)
        else:
            _GET(t)
            
        if len(ex) == 0:
            loopRunning = False
        else:
            t = ListPopFirst(ex)
            
    return

# cycles through the logic statement
# ex: list to take execution input from
def LogicLoop(ex):
    t = ListPopFirst(ex)
    loopRunning = True
    while loopRunning == True:
        z = convert(t)
        if t == 'and':
            _AND()
        elif t == 'or':
            _OR()
        elif t == 'not':
            _NOT()
        elif t == 'eq':
            _EQ()
        elif t == 'lt':
            _LT()
        elif t == 'gt':
            _GT()
        elif isNumber(z) or isBool(z):
            ListPush(operand,z)
        elif t == 'add':
            _ADD()
        elif t == 'sub':
            _SUB()
        elif t == 'mul':
            _MUL()
        elif t == 'div':
            _DIV()
        elif t == '{':
            logicTrue = []
            logicFalse = []
            c = ListPop(operand) # check if condition is true
            
            curly = 1
            t = ListPopFirst(ex)
            # Get True Logic Branch
            while curly > 0:
                ListPush(logicTrue,t)
                t = ListPopFirst(ex)
                if t == '{':
                    curly = curly + 1
                elif t == '}':
                    curly = curly - 1
            print(ex)
            print (logicTrue)
            t = ListPopFirst(ex)
            if t == 'if': # if this is only an if statement, we're done already!
                if c == True:
                    InterpretorLoop(logicTrue)
                    return
            elif t == '{': # Otherwise, get the false branch
                curly = 1
                while curly > 0:
                    ListPush(logicFalse,t)
                    t = ListPopFirst(ex)
                    if t == '{':
                        curly = curly + 1
                    elif t == '}':
                        curly = curly - 1
                t = ListPopFirst(ex)
                if t == 'ifelse' and c == False:
                    InterpretorLoop(logicFalse)
                    return
                elif t == 'ifelse' and c == True:
                    InterpretorLoop(logicTrue)
                    return
                else:
                    Debug("Invalid ifelse statement!")
            else:
                Debug("Invalid if statement!")
                
        t = ListPopFirst(ex)
                
    return
    

######## Main
# Controls the Program. Can accept filename as an argument, if not supplied will ask for a file.
if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = input ("Enter SPS File Name: ")
    L = parseFile(open(fn,"r"))
    print(L)
    InterpretorMain(L)
    printOutput()
