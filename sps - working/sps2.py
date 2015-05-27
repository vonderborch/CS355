#!/usr/bin/python3
import re
import sys
import types

######## Global Variables
# Stacks
dictionary = []
execution = []
operand = []
# Dictionary
tempDictionary = {}

# Sept 21, 2011 -- fixed the handling of }{ -- each brace should be a separate token
# A regular expression that matches postscript each different kind of postscript token
pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'

######## Debug Functions
def Debug(*s):
    print(s)
    print("REMAINING EXECUTION STACK:")
    for i in execution:
        print (i)
    sys.exit(1)
    return

######## Common Functions
#### Is Variable
# isNumber
def isNumber(x):
    if type(x) == int or type(x) == float:
        return True
    return False

# isBool
def isBool(x):
    if type(x) == bool:
        return True
    return False

# isString
def isString(x):
    if type(x) == str:
        return True
    return False
    
# isDict
def isDict(x):
    if type(x) is dict == False:
        return False
    return True

#### Convert Variable
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
def PopNumber(s,v):
    x = OperandPop()
    if isNumber(x) == False:
        Debug("%s in operation %s is not a number or doesn't exist!",v,s)
    return x;
def PopBoolean(s,v):
    x = OperandPop()
    if isBool(x) == False:
        Debug("%s in operation %s is not a boolean or doesn't exist!",v,s)
    return x;
def PopTwoNumbers(s):
    return (PopNumber(s,"x1"),PopNumber(s,"x2"));
def PopTwoBooleans(s):
    return (PopBoolean(s,"x1"),PopBoolean(s,"x2"));

######## SPS Functions
#### Number Operators
def _ADD(L):
    x1,x2 = PopTwoNumbers("_ADD")
    return OperandPush(x1 + x2)

def _SUB(L):
    x1,x2 = PopTwoNumbers("_SUB")
    return OperandPush(x1 - x2)

def _MUL(L):
    x1,x2 = PopTwoNumbers("_MUL")
    return OperandPush(x1 * x2)

def _DIV(L):
    x1,x2 = PopTwoNumbers("_DIV")
    return OperandPush(x1 / x2)

def _EQ(L):
    x1,x2 = PopTwoNumbers("_EQ")
    return OperandPush(x1 == x2)

def _LT(L):
    x1,x2 = PopTwoNumbers("_LT")
    return OperandPush(x1 < x2)

def _GT(L):
    x1,x2 = PopTwoNumbers("_GT")
    return OperandPush(x1 > x2)

#### Boolean Operators
def _AND(L):
    x1,x2 = PopTwoBooleans("_AND")
    return OperandPush(x1 and x2)

def _OR(L):
    x1,x2 = PopTwoBooleans("_OR")
    return OperandPush(x1 or x2)

def _NOT(L):
    return OperandPush(not PopBoolean("_OR","x"))

#### Stack Operators
def _DUP(L):
    t = OperandPop()
    OperandPush(t)
    OperandPush(t)
    return True

def _EXCH(L):
    t = OperandPop()
    OperandPushPosition(t, len(operand) - 1)
    return True

def _POP(L):
    return OperandPop()

def _GET(L):
    return True

#### Dictionary Creation
def _DICTZ(L):
    OperandPush({})
    return True

#### DICTIONARY MANIPULATION
def _BEGIN(L1,L2):
    t = OperandPop()
    if isDict(t) == False:
        Debug("No Dictionary on the Stack for _BEGIN!")
        return False
    DictionaryPush(t)
    return True

def _END(L):
    return ListPop(L)

#### Name Defination
def _DEF(L):
    t = {}
    tL = []
    t2 = ''
    t1 = ListPopFirst(L)
    if isString(t1) == False:
        Debug("T1 in operation _DEF is not a string!")

    temp = ListPopFirst(L)
    if temp != '{':
        t2 = temp
    else:
        tL.append(temp)
        curly = 1
        while curly > 0:
            x = ListPopFirst(L)
            tL.append(x)
            if x == '{':
                curly = curly + 1
            elif x == '}':
                curly = curly - 1
        temp = ListPopFirst(L)
        if temp != 'def':
            Debug("No def to end _DEF command!")

    if t2 != '':
        t = {t1:t2}
    else:
        t = {t1:tL}
    DictionaryPush(t)
    return True

#### Stack Printing
def _STACK(L):
    for i in L:
        print(i)
    return True

def _EQUALS(L):
    t = ListPop(L)
    print(t)
    return True

#### Sequencing Operators
def _IF(L):
    return True

def _IFELSE(L):
    return True

######## Stack Control
def ListPushItem(L,t,v):
    x = {t:value}
    L[len(dictionary)].append(x)
def ListPush(L,t):
    L.append(t)
def ListPop(L):
    if len(L) == 0:
        Debug("No item on the Selected Stack to pop!")
    return L.pop()
def ListPopFirst(L):
    if len(L) == 0:
        Debug("No item on the Selected Stack to pop!")
    return L.pop(0)
def ListPushPosition(L,t,p):
    L.insert(p,t)
    return t

def DictionaryPushItem(t,value):
    x = {t:value}
    dictionary[len(dictionary)].append(x)
def DictionaryPush(t):
    dictionary.append(t)
def DictionaryPop():
    if len(dictionary) == 0:
        Debug("No item on the Dictionary Stack to pop!")
    return dictionary.pop()

def ExecutionPush(t):
    execution.append(t)
def ExecutionPop():
    if len(execution) == 0:
        Debug("No item on the Execution Stack to pop!")
    return execution.pop()
def ExecutionPopFirst():
    if len(execution) == 0:
        Debug("No item on the Execution Stack to pop!")
    return execution.pop(0)

def OperandPush(t):
    operand.append(t)
    return t
def OperandPushPosition(t,p):
    operand.insert(p,t)
    return t
def OperandPop():
    if len(operand) == 0:
        Debug("No item on the Operand Stack to pop!")
    return operand.pop()

######## File Reader
# Given a string, return the tokens it contains
def parse(s):
   tokens = re.findall(pattern, s)
   return tokens

# Given an open file, return the tokens it contains
def parseFile(f):
   tokens = parse(''.join(f.readlines()))
   return tokens

######## Interpretor
def InterpretorMain(L):
    for word in L:
        ExecutionPush(word)
    InterpretorLoop()

def InterpretorLoop():
    t = ExecutionPopFirst()
    loopRunning = True
    while loopRunning == True:
        z = convert(t)
        if isNumber(z) or isBool(z):
            OperandPush(z)
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
        elif t == 'lt':
            _LT()
        elif t == 'gt':
            _GT()
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
        elif t == '/':
            _DEF()
        elif t == 'stack':
            _STACK()
        elif t == '=':
            _EQUALS()
        else:
            _GET()
            
        if len(execution) == 0:
            loopRunning = False
        else:
            t = ExecutionPopFirst()
        
######## Printing
def printOutput():
    print("OPERAND STACK:")
    _STACK()
    print("-----------------------")
    print("DICTIONARY STACK:")
    for i in dictionary:
        print(i)
        print("=======================")
    return

######## Main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = input ("Enter SPS File Name: ")
    L = parseFile(open(fn,"r"))
    print(L)
    InterpretorMain(L)
    printOutput()
