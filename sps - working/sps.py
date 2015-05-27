#!/usr/bin/python3
import re
import sys

######## Global Variables
# Stacks
dictionary = []
execution = []
operand = []

# Sept 21, 2011 -- fixed the handling of }{ -- each brace should be a separate token
# A regular expression that matches postscript each different kind of postscript token
pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'

######## Debug Functions
def Debug(*s):
    print(s)
    sys.exit(1)
    return

######## Common Functions
#### Is Variable
def isNumber(x):
    if type(x) is int == False or type(x) is float == False:
        return False
    else:
        return True

def isBool(x):
    if type(x) is bool == False:
        return False
    else:
        return True
    
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
#### Command Logic
def CommandLogic(t):
    if t == "add":
        _ADD()
        return True
    elif t == "sub":
        _SUB()
        return True
    elif t == "mul":
        _MUL()
        return True
    elif t == "div":
        _DIV()
        return True
    elif t == "eq":
        _EQ()
        return True
    elif t == "gt":
        _LT()
        return True
    elif t == "lt":
        _GT()
        return True
    elif t == "and":
        _AND()
        return True
    elif t == "or":
        _OR()
        return True
    elif t == "not":
        _NOT()
        return True
    elif t == "if":
        _IF()
        return True
    elif t == "ifelse":
        _IFELSE()
        return True
    return False

######## SPS Functions
#### Number Operators
def _ADD():
    x1,x2 = PopTwoNumbers("_ADD")
    return OperandPush(x1 + x2)

def _SUB():
    x1,x2 = PopTwoNumbers("_SUB")
    return OperandPush(x1 - x2)

def _MUL():
    x1,x2 = PopTwoNumbers("_MUL")
    return OperandPush(x1 * x2)

def _DIV():
    x1,x2 = PopTwoNumbers("_DIV")
    return OperandPush(x1 / x2)

def _EQ():
    x1,x2 = PopTwoNumbers("_EQ")
    return OperandPush(x1 == x2)

def _LT():
    x1,x2 = PopTwoNumbers("_LT")
    return OperandPush(x1 < x2)

def _GT():
    x1,x2 = PopTwoNumbers("_GT")
    return OperandPush(x1 > x2)

#### Boolean Operators
def _AND():
    x1,x2 = PopTwoBooleans("_AND")
    return OperandPush(x1 and x2)

def _OR():
    x1,x2 = PopTwoBooleans("_OR")
    return OperandPush(x1 or x2)

def _NOT():
    return OperandPush(not PopBoolean("_OR","x"))

#### Sequencing Operators
def _IF():
    t == ""
    while t != "{":
        CommandLogic(OperandPush(ExecutionPop()))
    if OperandPop() == True:
        OperandPush(ExecutionPop())
        ExecutionPop()
    return True

def _IFELSE():
    t == ""
    while t != "{":
        CommandLogic(OperandPush(ExecutionPop()))
    if OperandPop() == True:
        OperandPush(ExecutionPop())
        ExecutionPop()
    else:
        ExecutionPop()
        ExecutionPop()
        ExecutionPop()
        OperandPush(ExecutionPop())
        ExecutionPop()
    return True

#### Stack Operators
def _DUP():
    t = OperandPop()
    OperandPush(t)
    OperandPush(t)
    return True

def _EXCH():
    t = OperandPop()
    OperandPushPosition(t, len(operand) - 1)
    return True

def _POP():
    return OperandPop()

#### Dictionary Creation
def _DICTZ():
    t = {}
    DictionaryPush(t)
    return True

#### DICTIONARY MANIPULATION
def _BEGIN():
    if len(dictionary) < 1:
        Debug("No item on the Dictionary Stack for _BEGIN!")
        return False
    DictionaryPush(OperandPop())
    return

def _END():
    return DictionaryPop()

#### Name Defination
def _DEF():
    t1 = OperandPop()
    t2 = OperandPop()
    if type(t1) is str == False:
        Debug("T1 in operation _DEF is not a string!")
        return False
    t = [t1,t2]
    DictionaryPush(t)
    return True

#### Stack Printing
def _STACK():
    for i in operand:
        print(i)
    return True

def _EQUALS():
    t = OperandPop()
    print(t)
    return True

######## Stack Control
def DictionaryPushItem(t,value):
    x = {t:value}
    dictionary[len(dictionary)].append(x)
def DictionaryPush(t):
    dictionary.append(t)
def DictionaryPop():
    return dictionary.pop()

def ExecutionPush(t):
    execution.append(t)
def ExecutionPop():
    if len(execution) > 0:
        return execution.pop()
    else:
        printOutput()

def OperandPush(t):
    operand.append(t)
    return t
def OperandPushPosition(t,p):
    operand.insert(p,t)
    return t
def OperandPop():
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
    for w in L:
        ExecutionPush(w)
    InterpretorLoop()
    return

def InterpretorLoop():
    word = ExecutionPop()
    if word == None:
        return
    elif isBool(word) == True or isNumber(word) == True:
        OperandPush(word)
        InterpretorLoop()
    else:
        Interpretor(word)
        InterpretorLoop()

def Interpretor(w):
    if w.startswith('/') == True:
        t = w.split('/')
        word = ExecutionPop()
        if isBool(word) == True or isNumber(word) == True:
            DictionaryPushItem(t[1],x)
        else:
            tL = ["{"]
            i = 1
            while i > 0:
                word = ExecutionPop()
                if word == "{":
                    i = i + 1
                elif word == "}":
                    i = i - 1
                tL.append(word)
            while word != "def":
                word = ExecutionPop()
            DictionaryPushItem(t[1], tL)
    elif w == "add":
        _ADD()
    elif w == "sub":
        _SUB()
    elif w == "mul":
        _MUL()
    elif w == "div":
        _DIV()
    elif w == "eq":
        _EQ()
    elif w == "gt":
        _LT()
    elif w == "lt":
        _GT()
    elif w == "and":
        _AND()
    elif w == "or":
        _OR()
    elif w == "not":
        _NOT()
    elif w == "if":
        _IF()
    elif w == "ifelse":
        _IFELSE()
    elif w == "dup":
        _DUP()
    elif w == "exch":
        _EXCH()
    elif w == "pop":
        _POP()
    elif w == "dictz":
        _DICTZ()
    elif w == "begin":
        _BEGIN()
    elif w == "end":
        _END()
    elif w == "stack":
        _STACK()
    elif w == "=":
        _EQUALS()
    else:
        wordIntepretor(w)
    return 0

def wordInterpretor(w):
    L = dictionary[len(dictionary)].get(w)

    for word in L:
        if isBool(word) == True or isNumber(word) == True:
            OperandPush(word)
        else:
            if w.startswith('/') == True:
                t = w.split('/')
                word = L.pop()
                if isBool(word) == True or isNumber(word) == True:
                    DictionaryPushItem(t[1],x)
                else:
                    tL = ["{"]
                    i = 1
                    while i > 0:
                        word = ExecutionPop()
                        if word == "{":
                            i = i + 1
                        elif word == "}":
                            i = i - 1
                        tL.append(word)
                    while word != "def":
                        word = L.pop()
                    DictionaryPushItem(t[1], tL)
            elif w == "add":
                _ADD()
            elif w == "sub":
                _SUB()
            elif w == "mul":
                _MUL()
            elif w == "div":
                _DIV()
            elif w == "eq":
                _EQ()
            elif w == "gt":
                _LT()
            elif w == "lt":
                _GT()
            elif w == "and":
                _AND()
            elif w == "or":
                _OR()
            elif w == "not":
                _NOT()
            elif w == "if":
                _IF()
            elif w == "ifelse":
                _IFELSE()
            elif w == "dup":
                _DUP()
            elif w == "exch":
                _EXCH()
            elif w == "pop":
                _POP()
            elif w == "dictz":
                _DICTZ()
            elif w == "begin":
                _BEGIN()
            elif w == "end":
                _END()
            elif w == "stack":
                _STACK()
            elif w == "=":
                _EQUALS()
            else:
                wordIntepretor(w)
    

######## Printing
def printOutput():
    print("OPERAND STACK:")
    _STACK()
    print("-----------------------")
    print("DICTIONARY STACK:")
    for i in dictionary:
        print(i)
        print("=======================")
    sys.exit(1)
    return    

######## Main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = input ("Enter SPS File Name: ")
    L = parseFile(open(fn,"r"))
    print(L)
