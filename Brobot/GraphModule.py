from copy import deepcopy


class Edge:

	def __init__(self, moveNum, sourceState, targetState ):
		''' each edge contains the moveNum which is the move it takes to make this transition, as well as the target state '''
		self.moveNum = moveNum
		self.targetState = targetState
		self.sourceState = sourceState

	def __str__(self):
		return str(self.moveNum) + ", " + str(self.targetState)

	def __eq__(self, other):
		return self.moveNum == other.moveNum and self.targetState == other.targetState



class Graph:

	def __init__(self, board= None, graphDict = {}):
		self.graphDict = graphDict  # this dictionary represents the nodes and adjacency lists. Maps a state tuple to a list of edges
		self.duplicates = 0
		self.board = board
	
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
		newEdge = Edge(moveNum, state1, state2)
		if newEdge in self.graphDict[state1]:
			#print("duplicate edge!")
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
	
	def convertTupleToRobotDict(self, tuple):
		dict = {}
		dict[0] = (tuple[0], tuple[1])
		dict[1] = (tuple[2], tuple[3])
		dict[2] = (tuple[4], tuple[5])
		dict[3] = (tuple[6], tuple[7])
		return dict


	def shortestPath(self, startPositions):
	
		startState = self.convertRobotDictToTuple(startPositions)
		retrace = {}
		# a dictionary to retrace the steps through the bfs. key is state and value is edge that BROUGHT it here
		
		retrace[startState] = None # no move led to the start state
		q = []
		q += self.graphDict[startState] # fill the q with edges from start state
		#print(startState)
		while q != []:
			currentEdge = q.pop(0) # pop fron the front of the q
			currentState = currentEdge.targetState
			#print(currentState)
			if currentState in retrace:
				# already seen this state along a shorter path
				#print("already seen")
				continue
			retrace[currentState] = currentEdge
			if self.checkEndState(currentState):
				# we found the first end state, so return it
				shortest = self.bestSequence(retrace, currentState)
				return len(shortest), shortest
			# else add its edges to the q
			q += self.graphDict[currentState]
	
		print("error, didn't find an end state in the shortestPath method!")
		return float("inf"), None


	def bestSequence(self, retrace, endState):
		''' given the retrace dictionary and an endState, this method retraces the moves backwards and constructs
			the move sequence that leads to this end state '''
		currentState = endState
		sequence = []
		
		self.board.resetRobots(self.convertTupleToRobotDict(endState))
		#print("retracing best sequence")
		while True:
			
			#print(currentState)
			edge = retrace[currentState]

			if edge is None:
				# found the start of the sequence (aka the end of the retrace)
				return sequence
			
			move = edge.moveNum
			#print(move)
			sequence.insert(0, move)
			currentState = edge.sourceState


#	def stepBack(self, move):
#		''' given a move, this method does the OPPOSITE move to the current board to "step back" the move '''
#		if move % 2 == 0:
#			# an even number so add one to get the opposite
#			oppMove = move + 1
#		else:
#			oppMove = move - 1
#		self.board.makeMoveByInt(oppMove)
#		return self.convertRobotDictToTuple(self.board.robotPositions)

		

	def checkEndState(self, state):
		originalPositions = deepcopy(self.board.robotPositions)
		self.board.robotPositions = self.convertTupleToRobotDict(state)
		if self.board.endState():
			result = True
		else:
			result = False
		
		self.board.resetRobots(originalPositions)
		return result




