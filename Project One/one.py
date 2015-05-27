# Christian Webber
# August 30th, 2013
# Assignment 1

# Intended for Windows

debugging = False # Turn on or off test-specific pass/fail output
subDebugging = False # Turn on or off sub-function output

# Debugging output printer
# Input:
#   - s: the string to be outputted
# Returns:
#   - N/A
def debug(*s):
    if debugging == True:
        print(*s)
        
# Sub-Debugging output printer
# Input:
#   - s: the string to be outputted
# Returns:
#   - N/A
def subdebug(*s):
    if subDebugging == True:
        print(*s)

# Maps one string to another by character position.
# Input:
#   - s1: string to be mapped
#   - s2: string s1 is mapped to
# Returns:
#   - output: string s1 mapped to string s2
def makettable(s1,s2):
    output = {}
    i = 0
    for c in s1:
        output[c] = s2[i]
        i += 1
    subdebug(output)
    return output

# Translates a string argument according to the translation table.
# Input:
#   - ttable: the translation table
#   - s: the string to be translated
# Returns:
#   - output: s translated according to ttable
def trans(ttable,s):
    output = ""
    i = 0
    for c in s:
        output += ttable.get(c, c)
        i += 1
    subdebug(output)
    return output

# Creates a histogram from the given string
# Input:
#   - s: the string the histogram is created from
# Returns:
#   - output: the histogram, sorted by most frequent characters and
#               by most alphabetically (for = frequencies)
def histo(s):
    temp = {}
    for c in s:
        temp[c] = temp.get(c, 0) + 1
    subdebug(temp)
    output = sorted(temp.items(), key = lambda x: x[0])
    subdebug(output)
    output = sorted(output, key = lambda x: x[1], reverse = True)
    subdebug(output)
    return output

# Creates a digraph of the given string
# Input:
#   - s: the string to create the digraph from
# Returns:
#   - output: a digraph of the given string, sorted alphabetically
def digraphs(s):
    temp = {}
    maxchar = len(s) - 1
    for i, c in enumerate(s):
        if i != maxchar:
            ts = '/' + s[i] + s[i + 1] + '/'
            temp[ts] = temp.get(ts, 0) + 1
    subdebug(temp)
    output = sorted(temp.items(), key = lambda x: x[0])
    subdebug(output)
    return output

# Outputs text if allowed by debug settings
# Input:
#   - tID: Test ID string to output
#   - ga: the correct answer to the test
#   - ia: the answer the function tried to give that failed
# Returns:
#   - N/A
def testerOutput(tID, ga, ia):
    debug(s)
    debug(t)


# function to test translation code
# return True if successful, False if any test fails
def testtrans():
    ttable = makettable('abc', 'xyz')
    revttable = makettable('xyz', 'abc')
    #Test 1
    question = "Now I know the abc's!"
    answer = "Now I know the xyz's!"
    test = trans(ttable, question)
    if test != answer:
        testerOutput("T1 Failed", answer, test)
        return False
    #Test 2
    question = "Now I know the abc's!"
    answer = "Now I know the abc's!"
    test = trans(revttable, trans(ttable, question))
    if test != answer:
        testerOutput("T2 Failed", answer, test)
        return False
    #Test 3
    question = ''
    answer = ''
    test = trans(ttable, question)
    if test != answer:
        testerOutput("T3 Failed", answer, test)
        return False
    #Test 4
    question = "abc"
    answer = 'abc'
    test = trans(makettable('',''), "abc")
    if test != answer:
        testerOutput("T4 Failed", answer, test)
        return False
    #Test 5
    question = "Now I know my abc's!"
    answer = "Now I know my xyz's!"
    test = trans(ttable, question)
    if test != answer:
        testerOutput("T5 Failed", answer, test)
        return False
    #Test 6
    question = "Hello World!"
    answer = "Hello World!"
    test = trans(ttable, question)
    if test != answer:
        testerOutput("T6 Failed", answer, test)
        return False
    #Test 7
    question = "xy z abc d!x!a"
    answer = "xy z xyz d!x!x"
    test = trans(ttable, question)
    if test != answer:
        testerOutput("T7 Failed", answer, test)
        return False
    #Test 8
    question = "xy z abc d!x!a"
    answer = "ab c abc d!a!a"
    test = trans(revttable, question)
    if test != answer:
        testerOutput("T8 Failed", answer, test)
        return False
    return True


# function to test histo code
# return True if successful, False if any test fails
def testhisto():
    #Test 1
    question = "implemented"
    answer = [('e',3), ('m',2), ('d',1),('i',1), ('l',1), ('n',1), ('p',1), ('t',1)]
    test = histo(question)
    if test != answer:
        testerOutput("T1 Failed", answer, test)
        return False
    #Test 2
    question = "hello"
    answer = [('l',2), ('e',1), ('h',1), ('o',1)]
    test = histo(question)
    if test != answer:
        testerOutput("T2 Failed", answer, test)
        return False
    #Test 3
    question = "Bob"
    answer = [('B',1), ('b',1), ('o',1)]
    test = histo(question)
    if test != answer:
        testerOutput("T3 Failed", answer, test)
        return False
    #Test 4
    question = "Galactica"
    answer = [('a',3), ('c',2), ('G',1), ('i',1), ('l',1), ('t',1)]
    test = histo(question)
    if test != answer:
        testerOutput("T4 Failed", answer, test)
        return False
    #Test 5
    question = "hello there"
    answer = [('e',3), ('h',2), ('l',2), (' ', 1), ('o',1), ('r',1), ('t',1)]
    test = histo(question)
    if test != answer:
        testerOutput("T5 Failed", answer, test)
        return False
    return True


# function to test digraph code
# return True if successful, False if any test fails
def testdigraphs():
    #Test 1
    question = "A dig"
    answer = [('/ d/',1), ('/A /',1), ('/di/',1), ('/ig/',1)]
    test = digraphs(question)
    if test != answer:
        testerOutput("T1 Failed", answer, test)
        return False
    #Test 2
    question = "Hello Hello World"
    answer = [('/ H/', 1), ('/ W/', 1), ('/He/', 2), ('/Wo/', 1), ('/el/', 2), ('/ld/', 1), ('/ll/', 2), ('/lo/', 2), ('/o /', 2), ('/or/', 1), ('/rl/', 1)]
    test = digraphs(question)
    if test != answer:
        testerOutput("T2 Failed", answer, test)
        return False
    #Test 3
    question = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    answer = [('/ D/', 1), ('/ E/', 1), ('/ U/', 1), ('/ a/', 7), ('/ c/', 6), ('/ d/', 6), ('/ e/', 10), ('/ f/', 1), ('/ i/', 7), ('/ l/', 3), ('/ m/', 3), ('/ n/', 4), ('/ o/', 2), ('/ p/', 2), ('/ q/', 2), ('/ r/', 1), ('/ s/', 4), ('/ t/', 1), ('/ u/', 3), ('/ v/', 3), ('/, /', 4), ('/. /', 3), ('/Du/', 1), ('/Ex/', 1), ('/Lo/', 1), ('/Ut/', 1), ('/a /', 5), ('/a./', 1), ('/ab/', 3), ('/ad/', 2), ('/ae/', 1), ('/ag/', 1), ('/al/', 2), ('/am/', 3), ('/an/', 1), ('/ar/', 1), ('/at/', 8), ('/au/', 1), ('/bo/', 3), ('/ca/', 2), ('/cc/', 1), ('/ce/', 1), ('/ci/', 5), ('/co/', 4), ('/ct/', 1), ('/cu/', 2), ('/d /', 5), ('/da/', 1), ('/de/', 3), ('/di/', 2), ('/do/', 6), ('/du/', 1), ('/e /', 7), ('/ea/', 1), ('/ec/', 2), ('/ed/', 1), ('/eh/', 1), ('/ei/', 1), ('/el/', 2), ('/em/', 2), ('/en/', 4), ('/ep/', 2), ('/eq/', 1), ('/er/', 3), ('/es/', 3), ('/et/', 3), ('/eu/', 2), ('/ex/', 2), ('/ff/', 1), ('/fi/', 1), ('/fu/', 1), ('/g /', 1), ('/gi/', 1), ('/gn/', 1), ('/he/', 1), ('/i /', 2), ('/ia/', 4), ('/ic/', 2), ('/id/', 5), ('/il/', 1), ('/im/', 3), ('/in/', 7), ('/io/', 1), ('/ip/', 3), ('/iq/', 2), ('/ir/', 1), ('/is/', 5), ('/it/', 6), ('/iu/', 1), ('/la/', 5), ('/li/', 5), ('/ll/', 4), ('/lo/', 4), ('/lp/', 1), ('/lu/', 2), ('/m /', 6), ('/m,/', 1), ('/m./', 1), ('/ma/', 1), ('/mc/', 1), ('/me/', 1), ('/mi/', 1), ('/mm/', 1), ('/mo/', 3), ('/mp/', 1), ('/n /', 5), ('/na/', 1), ('/nc/', 1), ('/nd/', 1), ('/ng/', 1), ('/ni/', 5), ('/no/', 2), ('/ns/', 2), ('/nt/', 5), ('/nu/', 1), ('/o /', 3), ('/oc/', 1), ('/od/', 2), ('/of/', 1), ('/oi/', 1), ('/ol/', 6), ('/om/', 1), ('/on/', 4), ('/or/', 9), ('/os/', 1), ('/p /', 1), ('/pa/', 2), ('/pi/', 2), ('/po/', 1), ('/pr/', 2), ('/ps/', 1), ('/pt/', 2), ('/qu/', 5), ('/r /', 5), ('/r./', 1), ('/rc/', 1), ('/re/', 7), ('/ri/', 3), ('/ro/', 1), ('/ru/', 4), ('/s /', 3), ('/se/', 5), ('/si/', 4), ('/sm/', 1), ('/ss/', 1), ('/st/', 2), ('/su/', 2), ('/t /', 16), ('/t,/', 3), ('/t./', 1), ('/ta/', 3), ('/te/', 5), ('/ti/', 1), ('/tr/', 1), ('/tu/', 2), ('/u /', 1), ('/ua/', 2), ('/ud/', 1), ('/ug/', 1), ('/ui/', 4), ('/ul/', 3), ('/um/', 3), ('/un/', 3), ('/up/', 2), ('/ur/', 4), ('/us/', 1), ('/ut/', 3), ('/ve/', 2), ('/vo/', 1), ('/x /', 1), ('/xc/', 1), ('/xe/', 1)]
    test = digraphs(question)
    if test != answer:
        testerOutput("T3 Failed", answer, test)
        return False
    return True

# Performs, and prints results of, test
# Input:
#   - function: the function to test
#   - string: the test identification string
#   - passed: the string to be printed on a success
#   - failed: the string to be printed on a failure
# Returns:
#   - N/A
def testHelper(function, string, passed, failed):
    if function():
       print (passed % string)
    else:
       print (failed % string)
    print("")


# Main function for the project. Tests all sub-functions.
# Input:
#   - N/A
# Returns:
#   - N/A
if __name__ == '__main__':
    passedMsg = "%s passed"
    failedMsg = "%s failed"
    testHelper(testtrans, 'testtrans', passedMsg, failedMsg)
    testHelper(testhisto, 'testhisto', passedMsg, failedMsg)
    testHelper(testdigraphs, 'testdigraphs', passedMsg, failedMsg)


# Answer to the bonus cryptogram
thisIsTheCryptogramAnswer = """wikipedia: python became the chthonic enemy of the later olympian deity apollo, who slew him and remade his former home and the oracle, the most famous[2] in classical greece, as his own. changes such as these in ancient myths may reflect a profound change in the religious concepts of hellenic culture. some were gradual over time and others occurred abruptly following invasion."""
