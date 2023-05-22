import pandas as pd
import random
import string
from collections import deque
ohter = set(string.punctuation)
epsilon =  "ε" 
sigma = "Σ"
endMark = "$"
tableAux = (0,0)

def makeHash(P:list):
    grammar = {}
    grammar["P"] = P
    grammar["N"] = []
    grammar[sigma] = []
    grammar["S"] = "S"    
    for derivation in P:
        if derivation[0] not in grammar["N"]:
            grammar["N"].append(derivation[0])
        for i in derivation[1]:
            if i.isupper():
                if i not in grammar["N"]:
                    grammar["N"].append(i)
            else:
                if i not in grammar[sigma]:
                    grammar[sigma].append(i)
    return grammar

def firstTerminal(sigma:list):
    First = {}
    for i in sigma:
        First[i] = i
    return First

def firstNonterminal1aux(grammar,First,curr,visited):
    if curr not in visited:
        
        visited.append(curr)
        
    
    for i in grammar["P"]:
        if i[0] == curr:
            if i[1] == epsilon:       
                First[i[0]] = []
                First[i[0]].append(epsilon)
                break
            else:
                if len(i[1]) == 1 and i[1][0].isupper():
                    
                    if i[1] in First.keys():
                        
                        First[i[0]] = []
                        First[i[0]].append(epsilon)
                    else:
                        if i[1] in visited:
                            continue
                        else:
                            tup = firstNonterminal1aux(grammar,First,i[1],visited)
                            First = tup[0]
                            visited = tup[1]
                            if i[1] in First.keys():
                                
                                First[i[0]] = []
                                First[i[0]].append(epsilon)
                            else:
                                continue
                else:
                    for j in range(len(i[1])):
                        if i[1][j].isupper():
                            if i[1][j] in First.keys():
                                if j == len(i[1])-1:
                                    First[i[0]] = []
                                    First[i[0]].append(epsilon)
                                else:
                                        
                                    continue
                            else:
                                if i[1][j] in visited:
                                    break
                                else:
                                    tup = firstNonterminal1aux(grammar,First,i[1][j],visited)
                                    First = tup[0]
                                    visited = tup[1]
                                    if i[1][j] in First.keys():
                                        if j == len(i[1])-1:
                                            First[i[0]] = []
                                            First[i[0]].append(epsilon)
                                        else:
                                        
                                            continue
                                    else:
                                        break
                        else:
                            break
    return (First,visited)
                     
                        
def firstNonterminal1(grammar,First,visited=[]):
    
    for n in grammar["N"]:
        if n not in visited:
            tup = firstNonterminal1aux(grammar,First,n,visited)
            First = tup[0]
            visited = tup[1]
    return First
            
        

def firstNonterminal2(P:dict, First:dict, curr, visited=[]):
    if curr in visited:
        return First
    for derivation in P:
        if derivation[0] == curr:
            for symbol in derivation[1]:
                if symbol not in First.keys():
                    visited.append(curr)
                    First = firstNonterminal2(P, First, symbol)
                else:
                    if len(First[symbol]) == 1 and epsilon in First[symbol]:
                        if symbol == epsilon:
                            pass
                        else:
                            First = firstNonterminal2(P, First, symbol)
                try:
                    if First[derivation[0]]:
                        pass
                except:
                    First[derivation[0]] = []

                if symbol.islower():
                    visited.append(curr)
                    if symbol not in First[derivation[0]]:
                        First[derivation[0]].append(First[symbol])
                else:
                    visited.append(curr)
                    if First[symbol] not in First[derivation[0]]:
                        for i in First[symbol]:
                            if i not in First[derivation[0]]:
                                First[derivation[0]].append(i)
                if symbol != epsilon:
                    if epsilon not in First[symbol]:
                        break
    return First
        
    
def First(grammar:dict):
    First = {}
    First = firstTerminal(grammar[sigma])
    First = firstNonterminal1(grammar,First)        
    
    

    for derivation in grammar["P"]:
        First = firstNonterminal2(grammar["P"],First,derivation[0])
    return First


def Follow1(P):
    Follow = {}
    for derivation in P:
        Follow[derivation[0]] = []
    Follow["S"].append(endMark)
    return Follow
    
def Follow2(P,Follow,First):
    for derivation in P:
        for idx in range(len(derivation[1])):
            if idx != len(derivation[1])-1 and derivation[1][idx].isupper():
                for item in range(idx+1, len(derivation[1])):
                    for i in First[derivation[1][item]]:
                        if i != epsilon and i not in Follow[derivation[1][idx]]:
                            Follow[derivation[1][idx]].append(i)
                    if epsilon not in First[derivation[1][item]]:
                        break
    return Follow       


def Follow3(P,Follow,First):
    for derivation in P:
        for idx in range(len(derivation[1])):
            if idx == len(derivation[1])-1 and derivation[1][idx].isupper():
                for i in Follow[derivation[0]]:
                    if i != epsilon and i not in Follow[derivation[1][idx]]:
                        Follow[derivation[1][idx]].append(i)

            elif derivation[1][idx].isupper():
               if epsilon in First[derivation[1][idx+1]]:
                   for item in range(idx+1, len(derivation[1])):
                        for i in Follow[derivation[0]]:
                            if i != epsilon and i not in Follow[derivation[1][idx]]:
                                Follow[derivation[1][idx]].append(i)
                        if epsilon not in First[derivation[1][item]]:
                            break
    return Follow       

                            
                            
            
        
        
    

def Follow(grammar,First):
    Follow = Follow1(grammar["P"])
    Follow = Follow2(grammar["P"],Follow,First)
    Follow = Follow3(grammar["P"],Follow,First)
    return Follow


def ParsingTableaux(grammar):
    
    aux = [(0,0)]*len(grammar["N"])
    
    Terminal = [i for i in grammar["N"]]
    data = {}
    data[endMark] = aux
    for elem in grammar[sigma]:
        if elem == epsilon:
            continue

            
        else:
            data[elem] = aux
    Table = pd.DataFrame(data,index = Terminal)
    return Table

def ParsingTable(grammar,First,Follow):
    table  = ParsingTableaux(grammar)
    
    for derivation in grammar["P"]:
        if derivation[1] == epsilon:
            for i in Follow[derivation[0]]:
                table.loc[derivation[0],i] = derivation
                
        flag = False
        auxFirst = []
        for i in derivation[1]:
            if not i.isupper() :
                auxFirst.append(i)
                flag = True
                break
            else:
                for j in First[i]:
                    if j not in auxFirst:
                        if j != epsilon:
                            auxFirst.append(j)
                if epsilon not in First[i]:
                    flag = True
                    break
        if not flag:
            auxFirst.append(epsilon)      
        for terminal in auxFirst:
            if terminal == epsilon:
                continue
            if table.loc[derivation[0],terminal] != tableAux:
                if table.loc[derivation[0],terminal] == derivation:
                    continue
                else:
                    return None
            else:
                table.loc[derivation[0],terminal] = derivation
        if epsilon in auxFirst:
            for terminal in Follow[derivation[0]]:
                if table.loc[derivation[0],terminal] != tableAux:
                    if table.loc[derivation[0],terminal] == derivation:
                        continue
                    else:
                        return None
                else:  
                    table.loc[derivation[0],terminal] = derivation
    return table

def syntaxAnalisis(parsingTable,string):
    string = string+endMark
    stack = deque(['S',endMark])
    while stack[0] != endMark:
        if stack[0] == string[0]:
            stack.popleft()
            string = string[1:]
        elif not stack[0].isupper():
            return 'Syntax Error'
        elif parsingTable.loc[stack[0],string[0]] == tableAux:
            return 'Syntax Error'
        elif parsingTable.loc[stack[0],string[0]][0] == stack[0]:
            top = stack.popleft()
            if parsingTable.loc[top,string[0]][1] != epsilon:
                for i in ("".join(reversed(parsingTable.loc[top,string[0]][1]))):
                    stack.appendleft(i)
            else:
                continue
    return 'Accepted'


def eliminateLeft(X, P, grammar,visited=[], idx=[]):
    n = len(P)
    currNon = ''
    for derivation in range(len(P)):
        if P[derivation][0] == X:
            if X in P[derivation][1] and P[derivation][1].index(X) == 0:
                if currNon != '':
                    res = P[derivation][1][1:]
                    Z = currNon
                    P[derivation] = (Z.upper(), res+Z.upper())
                    #idx.append(P.index(P[derivation]))
                    
                    
                    
                else:
                    res = P[derivation][1][1:]
                    Z = random.choice(string.ascii_letters)
                    while Z.upper() == X or Z.upper() == 'S':
                        Z = random.choice(string.ascii_letters)
                    currNon = Z
                    grammar['N'].append(Z.upper())
                    P[derivation] = (Z.upper(), res+Z.upper())
                    if (Z.upper(),epsilon) not in P:
                        P.append((Z.upper(),epsilon))
                    #idx.append(P.index(derivation))
            
            elif P[derivation][1] == epsilon:
                Z = currNon
                P[derivation] = (X,Z.upper())
                #idx.append(P.index(P[derivation]))
                

            elif currNon != '':
                res = P[derivation][1]
                P[derivation] = (X, res + currNon.upper())

                    
                
                    
                    
   
    return P



def leftRecursion(grammar):
    nonterminals = grammar['N']
    for i in range(0,len(nonterminals)):
        Ai = nonterminals[i]
        for j in range(0,i):
            Aj = nonterminals[j]
            toReplace = [] 
            deltas = []
            for derivation in grammar['P']:
                if Ai == derivation[0]:
                    if derivation[1][0] == Aj:
                        toReplace.append(derivation)
                elif Aj == derivation[0]:
                    deltas.append(derivation[1])
            for derivation in toReplace:
                grammar['P'].remove(derivation)
                gamma = derivation[1][1:]
                for delta in deltas:
                    grammar['P'].append((Ai,delta+gamma))

        aux = eliminateLeft(Ai,grammar['P'],grammar)
        if aux == 'GRAMATICA CONTIENE EPSILON VAYA MAME':
            return grammar
        else:
            grammar['P'] = aux
    return grammar
                        

        
    
            


def Run():
    
    print("Enter the productions of your grammar, when you finish enter *")
    print(" ")
    p1 = input()
    P = []
    while p1 != '*':
        Nonterminal = p1[0]
        while "|" in p1:
            index = p1.index("|")
            curr = p1[0:index-1]
            p1 = p1[index+2:]
            try:
                index1 = curr.index(">")+1
                tup = (curr[0],curr[index1:])
                Nonterminal =  curr[0]
            except:
                tup = (curr[0],curr)
            P.append(tup)
        try:
            index = p1.index(">")+1
            tup = (p1[0],p1[index:])  
            P.append(tup)
            print("Another one...")
            p1 = input()
        except:
            tup = (Nonterminal,p1)  
            P.append(tup)
            print("Another one...")
            p1 = input()
    
    print("Here's your grammar")
    grammar = makeHash(P)
    print(" ")
    print(grammar)
    N = len(grammar['N'])
    grammar = leftRecursion(grammar)
    if N == len(grammar['N']):
        pass
    else:
        print(" ")
        print("Your grammar had left recursion...   NOT ANYMORE jijiji")
        print(grammar)
        print(" ")
        print(" ")
    print("Its First:")
    Firstx = First(grammar)
    print(Firstx)
    print(" ")
    print("Its Follow:")
    Followx = Follow(grammar,Firstx)
    print(Followx)
    print(" ")
    PredictiveParsingTable = ParsingTable(grammar,Firstx,Followx)
    try:
        
        if PredictiveParsingTable == None:
            print("ERROR: Your grammar it's not LL(1)")
    except:
    
        print("The Predictuve Parsing Table:")
        print(PredictiveParsingTable)
    
    print(" ")
    print("Now, you enter a string and i tell you if it's in your grammar ;)")
    
    flag = False
    while not flag:
        string = input()
        if string == "":
            flag = True
            print("Good Bye :D")
        else:
            print(syntaxAnalisis(PredictiveParsingTable,string))
    
            
    
    
    



Run()

    
    
            
            
            
            
            
            
        
    
            
                
            
                
            
            
            
                            
                            
                        
                   
                               
                        
                
                
        
        
    
                
        
        
            
            
            
                    
                        
                    
        

