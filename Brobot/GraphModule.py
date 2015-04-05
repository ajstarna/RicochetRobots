


class Edge:

	def __init__(self, moveNum, targetState):
		''' each edge contains the moveNum which is the move it takes to make this transition, as well as the target state '''
		self.moveNum = moveNum
		self.targetState = targetState

	def __str__(self):
		return str(self.moveNum) + ", " + str(self.targetState)



class Graph:

	def __init__(self, graphDict = {}):
		self.graphDict = graphDict  # this dictionary represents the nodes and adjacency lists. Maps a state tuple to a list of edges
	


	def addNode(self, state):
		''' given the state tupple that the new node will correspond to, adds the new node to the graph and adds the
			mapping to the nodeDict '''
		self.graphDict[state] = [] # no adjacent nodes to start


	def addEdge(self, state1, state2, moveNum):
		''' creates and adds an edge from state1 to state2 with the provided moveNum '''
		newEdge = Edge(moveNum, state2)
		self.graphDict[state1].append(newEdge)


	def createNodeFromDict(self, robotDict):
		''' given a robotDict from a board, creates a node in the dict with this state '''
		state = self.convertRobotDictToTuple(robotDict)
		self.addNode(state)


	def convertRobotDictToTuple(self, robotDict):
		result = ()
		for i in xrange(4):
			result += robotDict[i]
		return result


	def shortestPath(self, startPositions, pathLength):
		return float("inf"), None

	def convertTupleToRobotDict(self, stateTuple):
		return {}