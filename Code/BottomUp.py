import pandas as pd
import string
from collections import deque
ohter = set(string.punctuation)
epsilon =  "ε" 
sigma = "Σ"
endMark = "$"
dot = "•"

class Node:
    def __init__(self,state,kernel):
        self.state = state
        self.kernel = kernel
        self.nonKernel = []
        self.next = []
        
    def printNode(self):
        print(self.state)
        print(self.kernel)
        print(self.nonKernel)
        print(self.next)
        print(" ")
    
 
    

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

def checkKernels(lKernels:list, kernel:Node):
    for item in lKernels:
        if item[0].kernel == kernel.kernel:
            return True
    return False

def setItems(I:Node, P:list, created:list, lKernels:list, count=0):
    count+=1
    for item in I.kernel:
        for character in range(len(item[1])):
            if item[1][character] == dot and character == len(item[1])-1:
                if len(I.kernel) == 1:
                    return I, created, lKernels
                else:
                    continue
            if item[1][character] == dot and item[1][character+1].isupper():
                I.nonKernel = addItems(item[1][character+1],P, [])


    for item in I.nonKernel:
        for character in range(len(item[1])):
            if character == len(item[1])-1:
                break
            if item[1][character] == dot and item[1][character+1].isupper():
                elements = addItems(item[1][character+1],P, [])
                for element in elements:
                    if element not in I.nonKernel:
                        I.nonKernel.append(element)
    
    
    processed = []
    done = True
    for item in I.kernel + I.nonKernel:
        for character in range(len(item[1])):
            if item[1][character] == dot and character != len(item[1])-1:
                if item[1][character+1] not in processed:
                    processed.append(item[1][character+1])
                    itemAux = item[1].replace(item[1][character], "", 1)
                    itemAux = itemAux[:character+1] + dot + itemAux[character+1:]
                    nxt = Node(count, [(item[0], itemAux)])
                    count+=1
                    if nxt.kernel != I.kernel and not checkKernels(lKernels, nxt):
                        created.append([nxt])
                        lKernels.append([nxt])
                        I.next.append((nxt, (item[1][character+1])))
                    else:

                        if nxt.kernel == I.kernel:
                            if done:
                                I.next.append((I, (item[1][character+1])))
                                done = False
                        flag = True
                        for kernel in created:
                            if nxt.kernel == kernel[0].kernel:
                                flag = False
                                idx = created.index(kernel)
                                created.pop(idx)
                                Iaux, created, lKernels = setItems(kernel[0], P, created, lKernels)
                                I.next.append((Iaux,(item[1][character+1])))
                        if flag:
                            for kernel in lKernels:
                                if nxt.kernel == kernel[0].kernel and done:
                                    I.next.append((kernel[0], (item[1][character+1])))
                else:
                    count, nxt = toKernel(created, item, count)
                    for i in range(len(I.next)):
                        if I.next[i][1] == item[1][character+1]:
                            I.next[i][0].kernel.append(nxt)
                            if I.next[i][0].kernel == I.kernel:
                                I.next.remove(I.next[i])
                                I.next.append((I, (item[1][character+1])))
                                for pending in created:
                                    if pending[0].kernel == I.next[i][0].kernel:
                                        created.remove(pending)



    if len(I.next) == 0:
        I.next.append((None,None))
                
    return I, created, lKernels

def toKernel(created, item, count):
    
    for i in created:
        if i[0].kernel[0][0] == item[0]:
            for character in range(len(item[1])):
                    if item[1][character] == dot and character != len(item[1])-1:
                        itemAux = item[1].replace(item[1][character], "", 1)
                        itemAux = itemAux[:character+1] + dot + itemAux[character+1:]
                        count+=1
                    
            break
    return count, (item[0], itemAux)


def addItems(X, P:list, items=[]):
    for derivation in P:
        if derivation[0] == X:
            if derivation[1] == epsilon:
                items.append((derivation[0], dot))
            else:
                items.append((derivation[0], dot + derivation[1]))
    return items

def closure(P:list, head:Node, lKernels=[],  pending=[]):
    lKernels.append([head])
    pending.append([head])
    while len(pending) > 0:
        I = pending.pop(0)
        I, pending, lKernels = setItems(I[0], P, pending, lKernels) 

    return head


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
                    if First[symbol] not in First[derivation[0]]:
                        First[derivation[0]].append(First[symbol])
                else:
                    visited.append(curr)
                    if First[symbol] not in First[derivation[0]]:
                        for i in First[symbol]:
                            if i not in First[derivation[0]]:
                                First[derivation[0]].append(i)
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
        
        
        
        
        








def getStates(head:Node,count=1, visited=[]):
    p=[]
    for i in head.next:
        visited.append((i[0].kernel, i[1]))
        p.append(i)
    head, process = p.pop(0)
    i=0    
    while len(p) >= 0:
        head.state = count
        count+=1
        for i in head.next:
            if i != (None,None) and (i[0].kernel, i[1]) not in visited:
                visited.append((i[0].kernel, i[1]))
                p.append(i)
        try:
            head, process = p.pop(0)
        except:
            break
    return count
            
        
def parsingTableAux(grammar,state): 
    aux = ['_']*state
    
    states = [i for i in range(0,state)]
    goto = {}
    action = {}
    action[endMark] = aux
    for elem in grammar[sigma]:
        if elem == epsilon:
            continue

            
        else:
            action[elem] = aux
    for elem in grammar["N"]:
        goto[elem] = aux
        
    GoTo = pd.DataFrame(goto,index=states)
    Action = pd.DataFrame(action,index=states)
    return (Action,GoTo)

def checkP(item, p):
    for kernel in p:
        if (kernel[0].kernel, kernel[1]) == item:
            return True
    return False

def parsingTable(table,head:Node,P,follow,visited=[]):
    if len(head.next) == 0:
        if head.kernel[0] == ('T','S'+dot):
            table[0].loc[head.state,endMark] = 'acc'
            return table
        for kernel in head.kernel:
            for x in follow[kernel[0]]:
                for derivation in P:
                    if derivation == (kernel[0],kernel[1][0:len(kernel[1])-1]):
                        table[0].loc[head.state,x] = "r"+str(P.index(derivation))
        return table
    for kernel in head.kernel + head.nonKernel:
        if kernel[1][len(kernel[1])-1] == dot:
            for x in follow[kernel[0]]:
                for derivation in P:
                    if derivation == (kernel[0],kernel[1][0:len(kernel[1])-1]) or derivation == (kernel[0],epsilon):
                        table[0].loc[head.state,x] = "r"+str(P.index(derivation))
                        break
                                      
    p=[]
    for item in head.next:
        if not checkP(item, p):
            p.append(item)
    item = p.pop(0)
    while len(p) >= 0:
        
        if item[0] not in visited:
            visited.append(item[0])
            table = parsingTable(table ,item[0], P, follow, visited)
        
        if item[1].isupper():
            table[1].loc[head.state,item[1]] = "s"+str(item[0].state)
        else:
            table[0].loc[head.state,item[1]] = "s"+str(item[0].state)
        try:
            item = p.pop(0)
        except:
            break
    return table
   

def printTable(table,P):
    
    print("        ACTION              ")
    print(table[0])
    print(" ")
    print("              GoTo        ")
    print(table[1])   
    
def syntaxAnalisis(table,w,P):
    stack = [0]
    while(1):
        s = stack[len(stack)-1]
        a = w[0]
        if table[0].loc[s,a][0] == 's':
            
            stack.append(int(table[0].loc[s,a][1:]))
            
            w = w[1:]
        elif table[0].loc[s,a][0] == 'r':
            dex = P[int(table[0].loc[s,a][1:])]
            if dex[1] != epsilon:
                for x in range(len(dex[1])):
                    stack.pop(len(stack)-1)
            t = stack[len(stack)-1]
            
            toPush = int(table[1].loc[t,dex[0]][1:])
            stack.append(toPush)
            print("REDUCE with: "+dex[0]+"->"+dex[1])
            print(" ")
        elif table[0].loc[s,a] == 'acc':
            print("Accepted")
            break
        else:
            print("Syntax Error")
            break
            
             
        
        
    
    
    
def Run():
   
    R = [("S","VS"),("S",epsilon),("V","Di"),("D","Y"),("D",epsilon),("Y","UG"),("G","lUG"),("G",epsilon),("U","t"),("U","b"),("U","(Y)")]
    P = [('S','A'),('A','aA'),('A','a')]

    print("Here's your grammar")
    grammar = makeHash(P)
    print(" ")
    print(grammar)
    Firstx = First(grammar)
    print("Its Follow:")
    Followx = Follow(grammar,Firstx)
    print(Followx)
    print(" ")
    head = Node(0,[('T',dot+"S")])
    I = closure(P,head)
    print("Its Initial node of canonical LR(K):")
    I.printNode()
    print(" ")
    states = getStates(I)
    table = parsingTableAux(grammar,states)
    table = parsingTable(table,I,grammar['P'],Followx)
    print("Its Parsing Table:")
    printTable(table,grammar['P'])
    print(" ")
    print(" ")
    print("Now, you enter a string and i tell you if it's in your grammar ;)")
    print(" ")
    
    flag = False
    while not flag:
        string = input()
        if string == "":
            flag = True
            print("Good Bye :D")
        else:
            string = string+endMark
            syntaxAnalisis(table,string,grammar['P'])
    
Run()
#I.printNode()