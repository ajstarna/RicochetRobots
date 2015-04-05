


class Edge:

	def __init__(self, moveNum, targetState):
		''' each edge contains the moveNum which is the move it takes to make this transition, as well as the target state '''
		self.moveNum = moveNum
		self.targetState = targetState

	def __str__(self):
		return str(self.moveNum) + ", " + str(self.targetState)

	def __eq__(self, other):
		return self.moveNum == other.moveNum and self.targetState == other.targetState



class Graph:

	def __init__(self, graphDict = {}):
		self.graphDict = graphDict  # this dictionary represents the nodes and adjacency lists. Maps a state tuple to a list of edges
		self.duplicates = 0
	
	def numEdges(self):
		''' returns the total number of edges in the graph '''
		total = 0
		for list in self.graphDict.values():
			total += len(list)
		return total
		
	def printGraph(self):
		''' print out a representation of the graph '''
		for state in self.graphDict:
			line = str(state)
			for edge in self.graphDict[state]:
				line += " ---> " + str(edge)
			print(line)
		

	def addNode(self, state):
		''' given the state tupple that the new node will correspond to, adds the new node to the graph and adds the
			mapping to the nodeDict '''
		if state in self.graphDict:
			self.duplicates += 1
			return
		self.graphDict[state] = [] # no adjacent nodes to start


	def addEdge(self, state1, state2, moveNum):
		''' creates and adds an edge from state1 to state2 with the provided moveNum '''
		if not state1 in self.graphDict or not state2 in self.graphDict:
			print("Error adding edge from nonexisting node(s)")
			return
		newEdge = Edge(moveNum, state2)
		if newEdge in self.graphDict[state1]:
			print("duplicate edge!")
			return
		self.graphDict[state1].append(newEdge)


	def createNodeFromDict(self, robotDict):
		''' given a robotDict from a board, creates a node in the dict with this state 
			only create a node if this state doesn't already have a corresponding node in the graph'''
		state = self.convertRobotDictToTuple(robotDict)
		self.addNode(state)
	
	
	def createEdgeFromDicts(self, robotDict1, robotDict2, moveNum):
		''' given two robotDicts and a moveNumber, creates an edge from the first to second. 
			both states must already have a corresponding node in the graph '''
		state1 = self.convertRobotDictToTuple(robotDict1)
		state2 = self.convertRobotDictToTuple(robotDict2)
		self.addEdge(state1, state2, moveNum)


	def convertRobotDictToTuple(self, robotDict):
		result = ()
		for i in xrange(4):
			result += robotDict[i]
		return result


	def shortestPath(self, startPositions):
	
		startState = self.convertRobotDictToTuple(startPositions)
		
		return float("inf"), None





