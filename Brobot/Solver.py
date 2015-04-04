from Player import Player
from copy import deepcopy
import random
import time
import numpy as np

class Solver(Player):
	def __init__(self, board):
		Player.__init__(self, board)
	
	
	
	def play(self, timeLimit):
		n =len(self.board.robotPositions) #number of robot
		h = self.getHash()
		
		#transTable = np.ones((pow(pow(2,h),n),),dtype=np.int )
		#transTable = -1* transTable
		# initialize transposition table
		transTable = {}
		
		r = self.board.rows
		c = self.board.cols
		depth =1
		best =-1
		
		bestDepth=10000000
		tstart = time.clock()
		
		s =self.getState()
		
		transTable[s] = 0   # start state = 0
		
		op=deepcopy(self.board.robotPositions)
		
		queue = []
		
		queue.append(op)
		while len(queue)>0:
			
			
			if(time.clock()-tstart >= timeLimit):
				break
			cstate = queue.pop(0)	
			self.board.resetRobots(cstate)
			self.board.printBoard()
			depth = transTable[self.getState()] //100 # get current depth used for pruning
			
			if (self.board.endState()):
				if(bestDepth >= depth):
					bestDepth = depth +1
					best = self.getState()
#				a = getState()
				return bestDepth, best
			if( depth+1 >= bestDepth):
				continue
				
			for i in xrange(16): # try all moves at depth + 1
				
				t = self.makeMoveByInt(i)
				
				sc = self.getState()
				if (self.board.endState()):
					if(bestDepth >= depth):
						bestDepth = depth +1
						best = sc
					
					return bestDepth, best
				
					
				
				
				if(t and (not sc in transTable)):
					queue.append(deepcopy(self.board.robotPositions))
					transTable[self.getState()] = i  + (depth+1) * 100 # the move leads to this state
			#		if it has not been visisted then add it to queue 	
				self.board.resetRobots(cstate)
			
		self.transT=transTable
			
		return bestDepth, best
	
	
	
	def getState(self):
		j = self.getHash()
		sums=0
		for i in xrange(len(self.board.robotPositions)):
			sums+= pow(pow(2,j),i)* self.getScore(self.board.robotPositions[i][0],self.board.robotPositions[i][1])
		return sums
	
	
	
	
	
	def getSolution(self,transT,s):
	# reconstuct list of moves to the endstate using the transition table and  end state s (an integer)
		movelist = []
		self.setBoardByState(s)
		while (transT[s]!=0):
			moveId = transT[s]%100
			movelist.append(moveId)
			self.board.makeMoveByIntInverse(moveId)
		return movelist[::-1]
	
	
	
	def setBoardByState (self,s):
	#given a integer representing the state, reconstruct board using robotPositions and resetRobots
		h =self.getHash()	
		n = pow(2,h)	
		m = len(self.board.robotPositions)
		op=deepcopy(self.board.robotPositions)
		for i in xrange (m):
			p = s % n
			s = s // n
			r = p // self.board.cols
			c = p % self.board.cols
			op[i][0] =r
			op[i][1] =c
		self.board.resetRobots(op)
		return op
	
	def genMove(self):
		return 0
		
	def getHash(self):
		
		a = self.board.rows
		b = self.board.cols
		i =0
		while (pow(2,i)<a*b):
			i+=1
			
		return i
		
	def getScore(self,r,c):
		
		return r*(self.board.cols) + c
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
