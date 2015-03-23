from Player import Player
from copy import deepcopy
import random
import time
import numpy as np

class Solver(Player):
	def __init__(self, board):
		Player.__init__(self, board)
	
	
	
	def play(self, timeLimit):
		
		h = self.getHash()
		transTable = np.ones((pow(2,h),),dtype=np.int )
		transTable = -1* transTable
		r = self.board.rows
		c = self.board.cols
		
		
			
		s =self.getState()
		transTable[s] = 0
		
		op=deepcopy(self.board.robotPositions)
		
		queue = []
		
		queue.append(op)
		while len(queue)>0:
			if (self.board.endState()):
				
				a = getState()
				return a, transTable
			cstate = queue.pop(0)	
			self.board.resetRobots(cstate)
			
			
			for i in xrange(16):
				t = self.makeMoveByInt(i)
				
				if (self.board.endState()):
				
					a = getState()
					return a, transTable
				
					
				
				sc = self.getState()
				if(t and transTable[sc]==-1):
					queue.append(deepcopy(self.board.robotPositions))
					transTable[self.getState()] = i   # the move leads to this state
			#		if it has been visisted then add it to queue 	
				self.board.resetRobots(cstate)
			
			
			
		return None, None
	
	def getState(self):
		j = self.getHash()
		sums=0
		for i in xrange(len(self.board.robotPositions)):
			sums+= pow(pow(2,j),i)* self.getScore(self.board.robotPositions[i][0],self.board.robotPositions[i][1])
		return sums
	
	
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
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
