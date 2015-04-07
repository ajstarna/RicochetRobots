from Player import Player
import Board
from copy import deepcopy
import random
import time
import numpy as np
from GraphModule import Graph

class MCPlayer(Player):
	def __init__(self, board):
		Player.__init__(self, board)
		self.opp= deepcopy(self.board.robotPositions) # keep original position
	
	def play(self, timeLimit, numSamples, depth):
		''' override super '''
		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		bestSequence = None # this will be the best of all sequences found
		tStart = time.clock()
		
		while True:
			self.board.resetRobots(originalPositions)
			self.numMoves = 0
			while not self.board.endState():
				if bestSequence != None and len(currentSequence) >= len(bestSequence):
					# no need to keep looking on this path
					currentSequence = []
					self.board.resetRobots(originalPositions)
					continue
				
				newSequence = self.jumpAhead(numSamples, depth)
				currentSequence += newSequence

				if time.clock() - tStart >= timeLimit:
					
					self.board.resetRobots(originalPositions)
					if bestSequence == None:
						return [], float("inf")
					else:
						return bestSequence, len(bestSequence)
			
			# at this point it is an endstate
			
			if bestSequence == None:
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence
			elif len(bestSequence) > len(currentSequence):
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence


			currentSequence = []
			self.board.resetRobots(originalPositions)
	
	
	

	def findFirstSolutionNoTimeLimit(self, numSamples, depth):

		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		
		self.numMoves = 0
		while not self.board.endState():
			newSequence = self.jumpAhead(numSamples, depth)
			currentSequence += newSequence


		self.board.resetRobots(originalPositions) # don't want to actually change the board
		
		
		return currentSequence, len(currentSequence)



	def jumpAhead(self, numSamples, depth):
		''' n the number of samples.
			d the depth of each sample
		'''
		startPositions = deepcopy(self.board.robotPositions)
		currentValue = float("-inf") # there will always be a sequence that can beat negative infity score
		for i in xrange(numSamples):
			sequence = self.sample(depth)
			value = self.evaluateState()
			if value > currentValue:
				bestSequence = deepcopy(sequence)
				currentValue = value
			self.board.resetRobots(startPositions)

		# now play the moves from the best found sequence
		for move in bestSequence:
			self.board.makeMoveByInt(move)

		return bestSequence
	


	def sample(self, depth):
		sequence = []
		for i in xrange(depth):
			moveToMake = random.randint(0,15)
			sequence.append(moveToMake)
			self.board.makeMoveByInt(moveToMake)
			self.numMoves += 1
			if self.board.endState():
				break # don't move past an end state
		return sequence


	def evaluateState(self):
		heuristicList = []

		totalReachableTiles, sum = self.board.CalcReachability(True) # initialize the reachable field of each tile
		
		blueTile = self.board.getTileOfRobot(Board.Board.BLUE)
		
		# first deal with the reachibility from blue's tile
		currentReachability = blueTile.reachable
		if currentReachability == -1:
			# punish this heavily since if it is reachable then the answer is close (in this case not reachable)
			reachableScore = -1000
		else:
			# negate it since want to maximize score and lower reachability is better
			reachableScore = -1*currentReachability
		
		# add it to the heuristic list
		heuristicList.append(reachableScore)
		
		# now deal with the lower bound from blue's tile
		lowerBound = blueTile.lowerBound
		if lowerBound == -1:
			# this is really bad (and probably can't happen on a normal board
			lowerBoundScore = -10000
		else:
			lowerBoundScore = -1*lowerBound
		
		heuristicList.append(lowerBoundScore)
		
		# now deal with total number of reachable tiles
		totalReachableScore = totalReachableTiles # no need to negate this number since higher is better
		
		heuristicList.append(totalReachableScore)
		
		#print(heuristicList)
		heuristicArray = np.array(heuristicList)
		weightsArray = np.ones(heuristicArray.size) # try all weights the same for now
		
		#weightsArray[1] = 0 # turn off lower bound
		
		finalScore = np.sum(heuristicArray * weightsArray)
		
		return finalScore


	def pruneSequence(self,seq):
		
		newseq = deepcopy(seq)
		
		index =0
		while (index<len(newseq)):
			self.board.resetRobots(self.opp)
			newseq2 = deepcopy(newseq)
			newseq2.pop(index)
			self.playseq(newseq2)
			if(self.board.endState()):
				newseq = newseq2
				index -=1
			
				
			 
			index +=1
		return newseq
	
	def playseq(self,seq):
		
		for i in seq:
			self.board.makeMoveByInt(i)




####################################################################################
#############################     PNGS Player     ###############################
####################################################################################

class PNGSPlayer(MCPlayer):
	''' this class extends the MCPlayer to use the PNGS '''



	def play(self, timeLimit, numSamples, depth):
		''' override super '''
		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		bestSequence = None # this will be the best of all sequences found
		tStart = time.clock()
		
		while True:
			self.board.resetRobots(originalPositions)
			self.numMoves = 0
			while not self.board.endState():
				if bestSequence != None and len(currentSequence) >= len(bestSequence):
					# no need to keep looking on this path
					currentSequence = []
					self.board.resetRobots(originalPositions)
					continue
				
				newSequence = self.jumpAhead(numSamples, depth)
				currentSequence += newSequence

				if time.clock() - tStart >= timeLimit:
					
					self.board.resetRobots(originalPositions)
					if bestSequence == None:
						return [], 0
					else:
						return bestSequence, len(bestSequence)
			
			# at this point it is an endstate
			
			if bestSequence == None:
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence
			elif len(bestSequence) > len(currentSequence):
				#print("Updating best sequence with length of {0}".format(len(self.currentSequence)))
				bestSequence = currentSequence


			currentSequence = []
			self.board.resetRobots(originalPositions)



	def findFirstSolutionNoTimeLimit(self, numSamples, depth):

		originalPositions = deepcopy(self.board.robotPositions) # keep the original positions for resetting the board
		currentSequence = [] # keep track of the sequence of moves that brought us to current state
		
		self.numMoves = 0
		while not self.board.endState():
			newSequence = self.jumpAhead(numSamples, depth)
			currentSequence += newSequence


		self.board.resetRobots(originalPositions) # don't want to actually change the board
					
		print("original sequence length = {0}".format(len(currentSequence)))
		# try to improve on the found solution PNGS
		pngsSamples = 0
		pngsdepth =0
		tStart = time.clock()
		change, newSequence = self.pngs(currentSequence, pngsSamples, pngsdepth)
		print("time for improvement = {0}".format(time.clock()-tStart))
		if change:
			#print("PNGS Success!")
			return newSequence, len(newSequence)
		else:
		
			return currentSequence, len(currentSequence)
	
	
	

	def pngs(self, sequence, numSamples, depth):
		''' plan neighbourhood graph search:
			given a solution sequence of moves, this method will search around each state to expand the graph, 
			and then before a shortest path search from the source to any end state to try and improve the solution.
			return True if improved or False if didn't and the new(or old) sequence'''

		graph = Graph(self.board)
		
		originalPositions = deepcopy(self.board.robotPositions)
		
		graph.createNodeFromDict(self.board.robotPositions) # add the start node
		self.expandFromCurrent(graph, numSamples, depth) # add the start state
		
		for number in sequence:
			previousPosition = deepcopy(self.board.robotPositions)
			self.board.makeMoveByInt(number)	# get to the next state
			graph.createNodeFromDict(self.board.robotPositions) # add the new node
			graph.createEdgeFromDicts(previousPosition, self.board.robotPositions, number)
			self.expandFromCurrent(graph,  numSamples, depth)		# expand around the new state
		

		# now find the shortest path from start to any end state
		oldLength = len(sequence)
		newLength, newSequence = graph.shortestPath(originalPositions)


		self.board.resetRobots(originalPositions)

		#print("Graph has {0} nodes at end".format(len(graph.graphDict)))
		#print("Number of state duplicates = {0}".format(graph.duplicates))
		#print("Number of edges in graph = {0}".format(graph.numEdges()))
		#graph.printGraph()
		if newLength < len(sequence):
			return True, newSequence
		else:
			return False, sequence # no new path found



	def expandFromCurrent(self, graph, numSamples, depth):
		''' this method will take a graph
			it will expand the graph around this node. eventually reverts the board before returning
			so the next move can be made '''

		#originalPositions = deepcopy(self.board.robotPositions)


		
		savePositions = deepcopy(self.board.robotPositions)
		for i in xrange(numSamples):
			for d in xrange(depth):
				previousPosition = deepcopy(self.board.robotPositions)
				moveToMake = random.randint(0,15)
				self.board.makeMoveByInt(moveToMake)
				graph.createNodeFromDict(self.board.robotPositions)
				graph.createEdgeFromDicts(previousPosition, self.board.robotPositions, moveToMake)
			self.board.resetRobots(savePositions)
			
			
		#self.board.resetRobots(originalPositions)







