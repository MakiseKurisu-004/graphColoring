from itertools import combinations

class Graph:
    def __init__(self, numberOfNodes, inputEdges):
        '''
        \nParameters: 
        \nnumberOfNodes - it's exactly how it sounds
        \ninputEdges - the currently existing edges on your graph
        '''
        self.numberOfNodes = numberOfNodes
        self.inputEdges = inputEdges
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
            self.graphColoring()
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
    
    def graphColoring(self):
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
    
    def printResults(self):
        '''
        Function:
        Prints the results of the function
        '''
        for i in self.colored:
            self.results.append(self.coveringTable[str(i)])
        print(f"Results:\nThis graph can be colored with {len(self.colored)} colors.\nThe nodes that'll be colored with the same color are: ")
        for i in range (len(self.results)):
            print("{}.{}".format(i + 1, self.results[i]))
