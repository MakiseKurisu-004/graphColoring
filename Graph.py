from itertools import combinations, permutations
from random import randint

class Graph:
    def __init__(self, numberOfNodes, inputEdges, method = 'deterministic', typeOfResult = 'understandable'):
        '''
        \nParameters: 
        \nnumberOfNodes - it's exactly how it sounds
        \ninputEdges - the currently existing edges on your graph
        \nmethod - 'heuristic' or 'deterministic'
        \ntypeOfResult - only necessary for deterministic method\n
                        'understandable', 'anyPossible', 'random', 'allPossible'
        '''
        self.numberOfNodes = numberOfNodes
        self.inputEdges = inputEdges
        self.tor = typeOfResult
        self.nodes = []
        self.edges = []
        self.all_Possible_Edges = []
        self.mis = []
        self.coveringTable = {}
        self.pos = ''
        self.posList = []
        self.colored = []
        self.results = []
        if numberOfNodes and inputEdges:
            self.nodesListCreator()
            self.edgeListCreator()
            self.allPossibleEdges()
            self.maximumIndependentSet()
            self.petrick()
            if method == 'heuristic':
                self.graphColoringHeuristic()
                self.printResults()
            if method == 'deterministic':
                self.graphColoringDeterministic()
                self.printResults()
        else:
            print("Enter the number of nodes and the edges")


    def nodesListCreator(self):
        '''
        Function: 
        Returns a list of the nodes in the from 1 to x where x is the number of nodes
        '''
        self.nodes=[x for x in range(1, self.numberOfNodes + 1)]
    
    def edgeListCreator(self):
        '''
        Function: 
        Turns the input list into a list of lists of ints. The nested lists are the edges.
        '''
        edgeList = [list(edge) for edge in self.inputEdges]
        self.edges = [[int(num) for num in edge] for edge in edgeList]
        for edge in self.edges:
            edge.sort()
    
    def allPossibleEdges(self):
        '''
        Function:
        Returns a list of all possible edges in the graph
        '''
        allPossibleEdges2 = combinations(self.nodes, 2)
        self.all_Possible_Edges = [list(edges) for edges in allPossibleEdges2]
        for edge in self.all_Possible_Edges:
            edge.sort()
    
    def maximumIndependentSet(self):
        '''
        Function: 
        Finds the MIS and returns it in the MIS attribute
        '''
        for edge1 in self.all_Possible_Edges:
            if edge1 not in self.edges:
                self.mis.append(edge1)
            else: 
                pass

    def petrick(self):
        '''
        Function: 
        Turns the covering table into pos in string and list form
        '''
        change = 0
        for i in range(1, self.numberOfNodes + 1):
            for edge in self.mis:
                if edge[0] == i:
                    self.coveringTable[str(i+change)] = edge
                    change += 1
                else:
                    pass
            change -= 1
        for i in range(1, self.numberOfNodes + 1):
            self.pos += '('
            self.posList.append([])
            for edge in self.coveringTable.values():
                if i in edge:
                    key = list(self.coveringTable.values()).index(edge)
                    self.pos += list(self.coveringTable.keys())[key]+ ' + '
                    self.posList[i-1].append(list(self.coveringTable.keys())[key])
            self.pos = self.pos[:-3]
            self.pos += ')'
    
    def graphColoringHeuristic(self):
        '''
        Function:
        Heuristically solves graph coloring problem
        '''
        tempList = self.posList
        color = []
        for i in range(1, self.numberOfNodes + 1):
            for sum in tempList:
                if str(i) in sum: 
                    inx = tempList.index(sum)
                    tempList[inx].clear()
                    color.append(i)
        self.colored = []
        [self.colored.append(x) for x in color if x not in self.colored]

    def graphColoringDeterministic(self):
        paths = list(permutations(self.nodes))
        colorLists = []
        for path in paths:
            tempList = self.posList.copy()
            color = []
            for i in path:
                for sum in tempList:
                    if str(i) in sum: 
                        inx = tempList.index(sum)
                        tempList[inx] = []
                        color.append(i)
            colored = []
            [colored.append(x) for x in color if x not in colored]
            colorLists.append(colored)
        lenList = []
        for lists in colorLists:
            lenList.append(len(lists))
        lenList = [x for x in lenList if x]
        small = min(lenList)
        if self.tor == 'anyPossible':
            small = lenList.index(small)
            self.colored = colorLists[small]
        else:
            indices = []
            for i in range(len(lenList)):
                if lenList[i] == small:
                    indices.append(i)
            minColor = []
            for i in indices:
                minColor.append(colorLists[i])   
            self.colored = minColor

    def printResults(self):
        '''
        Function:
        Prints the results of the function
        '''
        def ifList(testList):
            for i in testList:
                if isinstance(i, list) == True:
                    return True
            return False
    
        if ifList(self.colored) == True:
            if self.tor == 'random':
                inx = randint(0,len(self.colored))
                for i in self.colored[inx]:
                    self.results.append(self.coveringTable[str(i)])
                print(f"Results:\nThis graph can be colored with {len(self.colored)} colors.\nThe nodes that'll be colored with the same color are: ")
                for i in range (len(self.results)):
                    print("{}.{}".format(i + 1, self.results[i]))
            elif self.tor == 'allPossible':
                for j in self.colored:
                    for i in j:
                        self.results.append(self.coveringTable[str(i)])
                    print(f"Results:\nThis graph can be colored with {len(self.colored)} colors.\nThe nodes that'll be colored with the same color are: ")
                    for i in range (len(self.results)):
                        print("{}.{}".format(i + 1, self.results[i]))
            elif self.tor == 'understandable':
                resultsList = []
                betterResultsList = []
                for color1 in self.colored:
                    for i in color1:
                        resultsList.append(self.coveringTable[str(i)])
                print('Calculating...')
                for color2 in resultsList:
                    for color1 in resultsList:
                        if not any(item in color1 for item in color2):
                            betterResultsList.append(color1)
                            betterResultsList.append(color2)
                brl = set(tuple(x) for x in betterResultsList)
                bestResultsList = [list(x) for x in brl]
                inx = randint(0,len(bestResultsList))
                for i in bestResultsList[inx]:
                    self.results.append(self.coveringTable[str(i)])
                print(f"Results:\nThis graph can be colored with {len(self.colored)} colors.\nThe nodes that'll be colored with the same color are: ")
                for i in range (len(self.results)):
                    print("{}.{}".format(i + 1, self.results[i]))


        if ifList(self.colored) == False:
            for i in self.colored:
                self.results.append(self.coveringTable[str(i)])
            print(f"Results:\nThis graph can be colored with {len(self.colored)} colors.\nThe nodes that'll be colored with the same color are: ")
            for i in range(len(self.results)):
                print("{}.{}".format(i + 1, self.results[i]))
