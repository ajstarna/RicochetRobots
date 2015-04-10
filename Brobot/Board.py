import numpy as np
import Tile
import random
import Move
from copy import deepcopy

class Board:
	''' the Board class. to be treated as an abstract class. Use a subclass for the actual board with more
		specific behaviour '''
	BLUE = 0
	RED = 1
	GREEN = 2
	YELLOW = 3
	
	conversionDict = {"BLUE":0, "RED":1, "GREEN":2, "YELLOW":3}


	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.allMoves = Move.AllMoves()
		self.previousMove = None

	def initializeTiles(self):
		''' this method initializes the array of tiles randomly.
			this includes wall placement but not robots or targets '''
		raise NotImplementedError("Please implement this method")

	def initializeTargetPositions(self):
		''' this method places the 17 targets on the board.
			consider an abstract method '''
		raise NotImplementedError("Please implement this method")
	
	
	def setTarget(self):
		''' this method will pick a random target from the target list and make that the currentTarget for the game '''
		
		self.currentTarget = self.targetPositions.pop()
		self.array[self.currentTarget[0], self.currentTarget[1]].target = True
		
		
	def initializeRobotPositions(self):
		''' this method places the four robots randomly on the board.
			self.array gets updated such that the four tiles know they posses a robot, and
			a dictionary containing the robot positions is return '''
		robotPositions = dict()
		for robot in xrange(4):
			# the while loop ensures that robots have unique positions.
			while(True):
				iCoord = random.randint(0, self.rows-1)
				jCoord = random.randint(0, self.cols-1)
				if (iCoord, jCoord) in robotPositions.values():
					continue # another robot is already at this position so try again
				elif self.array[iCoord, jCoord].target != None:
					continue
				else:
					robotPositions[robot] = (iCoord, jCoord)
					self.array[iCoord, jCoord].robot = robot
					break # move onto the next robot in the outer for loop
		return robotPositions
	
	
	def printBoard(self):
		''' this method displays a board state '''
		result = "*"
		for i in xrange(self.cols):
			result  += "-*"
		print(result)
		for i in xrange(self.rows):
			result1 ="|"
			result2 = "*"
			for j in xrange (self.cols):
				'''checking tile content'''
				if (self.array[i,j].robot==None):
					
					if (self.array[i,j].target == True):
						result1 += "X"
					else:
						result1 +=" "
				elif (self.array[i,j].robot==0):
					result1 += "B"
				elif (self.array[i,j].robot==1):
					result1 += "R"
				elif (self.array[i,j].robot==2):
					result1 += "G"
				elif (self.array[i,j].robot==3):
					result1 += "Y"
				'''checking east wall'''
				if(self.array[i,j].wallDict["EAST"]==True):
					result1+="|"
				else :
					result1+= " "
				'''checking south wall'''
				if(self.array[i,j].wallDict["SOUTH"]==True):
					result2+="-*"
				else :
					result2+= " *"
			print(result1)
			print (result2)


	def validMove(self, moveInt):
		''' returns whether the move is valid or not.
			i.e. will the robot actual move at all. '''
		move = self.allMoves.getMoveAtIndex(moveInt)
		position = self.robotPositions[move.colour]
		tile = self.array[position]
		if tile.wallDict[move.direction]:
			return False # there is a wall in the way!

		adjacentTile = self.getAdjacentTile(tile, move.direction)
		if adjacentTile is None:
			return False # just to be safe, however at this point since there is no wall in that direction, the
						 # adjacent tile shouldn't be none
						 
		if not adjacentTile.robot is None:
			return False # a robot in the way!

		return True # nothing in the way


	
	

	def makeMoveByInt(self, moveInt):
		''' this method will take an integer and make the move that that integer corresponds to.
			in this way, we can store moves as just an integer and convert them as needed.
			board will contain an AllMoves object where the move is grabbed from '''
		move = self.allMoves.getMoveAtIndex(moveInt)
		self.previousMove = moveInt # set the previous move
		return self.makeMove(move)
	
	
	def makeRandomMove(self):
		''' this method will make a random VALID move and return the move number.
			we can call this move instead of doing a possible "useless" move '''
		opposite = self.allMoves.getOppositeMove(self.previousMove)
		while True:
			moveToMake = random.randint(0,15)
			if moveToMake == opposite:
				continue # would be foolish to move one way then back again right after
			if self.validMove(moveToMake):
				break
			# otherwise not valid so keep looking
			
		# found a valid move that isn't the opposite of the previous move, so make it
		self.makeMoveByInt(moveToMake)
		return moveToMake
		
		
	
	
	def makeMoveByIntInverse(self, moveInt):
		''' this method will take an integer and make the inverse move that that integer corresponds to.
			in this way, we can store moves as just an integer and convert them as needed.
			board will contain an AllMoves object where the move is grabbed from '''
		move = self.allMoves.getMoveAtIndex(moveInt)
		if(move.direction == 'NORTH'):
			move.direction='SOUTH'
		elif (move.direction == 'WEST'):
			move.direction='EAST'
		elif (move.direction == 'SOUTH'):
			move.direction='NORTH'
		else:
			move.direction='WEST'
		print (move)
		return self.makeMove(move)
		
		

	def makeMove(self, move):
		''' given a move, make it on the board (so move the colour in the direction and update the array) 
			if no movement is possible then False is returned to indicate nothing happend, otherwise True is returned'''

		
		startPosition = self.robotPositions[move.colour] # initalize the endPosition to be the starting position
		
		#print("Start position = {}".format(startPosition))
		# now see how far the robot can move in the direction
		currentTile = self.array[startPosition]
		
		somethingHappend = False
		while True:
			if currentTile.wallDict[move.direction]:
				# there is a wall in the direction we need to move, so final spot
				break
			
			# since an edge tile will always have a wall, if we made it to here then we know we can find the adjacent tile
			adjacentTile = self.getAdjacentTile(currentTile, move.direction)
			if adjacentTile.robot != None:
				# there is a robot blocking us, so final spot
				break

			somethingHappend = True # the robot was able to move at least one tile
			
			# no wall or robot in the way, so move the robot onto the adjacent tile
			adjacentTile.robot = currentTile.robot
			currentTile.robot = None
			self.robotPositions[move.colour] = adjacentTile.position
			currentTile = adjacentTile

		# the currentTile is the ending position
		return somethingHappend
		

	
		
	def getAdjacentTile(self, tile, direction):
		''' given a tile and a direction, this returns the tile adjacent in that direction.
			return None if an edge '''
		i, j = tile.position
		if direction == "NORTH" or direction ==0:
			i -= 1
		elif direction == "SOUTH" or direction == 2:
			i += 1
		elif direction == "EAST" or direction ==1:
			j += 1
		elif direction == "WEST" or direction ==3:
			j -= 1

		if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
			# out of bounds
			return None
			
		return self.array[i,j]



	def endState(self):
		''' returns boolean of whether the board is in an end state (i.e. is the right robot at the target '''
		try:
			return self.currentTarget == self.robotPositions[0] #we assume blue is always the target robot
		except:
			# currentTarget not set yet
			print("currentTarget not yet set!")
			return False


	def resetRobots(self, resetPositions):
		''' this method takes a dictionary with robot positions to set self.robot positions to.
			it does that as well as updating the tiles in the array to reflect the change. '''
		
		#print("start of resetrobots: self.robotPositions = {0}, resetPositions = {1}".format(self.robotPositions, resetPositions))
		
		for i in xrange(4):
			originalPosition = self.robotPositions[i]
			originalTile = self.array[originalPosition]
			if not originalTile.position in resetPositions.values():
				originalTile.robot = None
			#print("original Tile = {0}".format(originalTile))
			newPosition = resetPositions[i]
			newTile = self.array[newPosition]
			newTile.robot = i
			#print("new tile = {0}".format(newTile))
		
			self.robotPositions[i] = resetPositions[i]#(resetPositions[i][0], resetPositions[i][1])
			#print("start of resetrobots: self.robotPositions = {0}, resetPositions = {1}".format(self.robotPositions, resetPositions))
			#print()
			#print()
	

		#self.robotPositions = deepcopy(resetPositions)
		
		

	def validateMoveSequence(self, sequence):
		''' takes a move sequence (as integers!) as input as validates if it results in an end state '''
		resetPositions = deepcopy(self.robotPositions)
		
		for i in sequence:
			self.makeMoveByInt(i)

		valid = self.endState()
		#print("robot positions after making moves in validateMoveSequence = {0}".format(self.robotPositions))
		self.resetRobots(resetPositions)
		return valid



	def getTileOfRobot(self, robot):
		''' given a robot (integer) returns the tile which it is occupying '''
		position = self.robotPositions[robot]
		return self.array[position]
	


	def correctRobotTiles(self):
		''' a debugging method to see if all 4 robots are accounted for on a tile '''
		robots = {}
		for j in xrange(16):
			for k in xrange(16):
				if self.array[j,k].robot != None:
					robots[self.array[j,k].robot] = (j,k)
					#print("Tile at {0},{1} has robot = {2}".format(j, k, self.array[j,k].robot))

		if len(robots) != 4:
			print("Too few tiles think they have a robot! {0}".format(robots))
			return False
		return True




	def getRay(self,r,c,direction):
		''' returns a list of tile that casts from (r,c) in a direction
		until a wall is present
		not including tile(r,c) itself
			0 = NORTH
			1 = EAST
			2 = SOUTH
			3 = WEST
		
		'''
		
		ray =[]
		currentTile = self.array[r,c]
		if (direction ==0 and not currentTile.wallDict["NORTH"]  ): #NORTH
			
			currentTile = self.array[r-1,c]
			while (not currentTile.wallDict["NORTH"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[currentTile.position[0]-1,c]
			ray.append(currentTile)
		elif (direction == 1 and not currentTile.wallDict["EAST"]): # EAST
			currentTile = self.array[r,c+1]
			while (not currentTile.wallDict["EAST"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r,currentTile.position[1]+1]	
			ray.append(currentTile)
		elif (direction == 2 and not currentTile.wallDict["SOUTH"]): # SOUTH
			currentTile = self.array[r+1,c]
			while (not currentTile.wallDict["SOUTH"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[currentTile.position[0]+1,c]
			ray.append(currentTile)	
		elif (direction == 3 and not currentTile.wallDict["WEST"]): # WEST- 
			currentTile = self.array[r,c-1]
			while (not currentTile.wallDict["EAST"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r,currentTile.position[1]-1]	
			ray.append(currentTile)
		return ray	
	
	
	def paintLB(self,tileList, LB):
		'''recursive function to calculate lowerbound on each tile, 
		each tile should starte with score -1
		at the end of the function, if some tile was not visited ,
		that means it is not reachable from the target tile
		thus would also have a score of -1
		
		input arguement should be the a list of first four lines of tiles in the four direction of the target tile
		'''
		if (not tileList):# if the queue is empty return none
			return
		newList =[]
		for tile in tileList:# each tile at this level (distance away from target)
			
			r = tile.position[0]
			c = tile.position[1]
			if (not tile.wallDict["NORTH"]):## check  all the tile to the north direction of the current tile
				temp = self.array[r-1,c] ## move one tile to the north
				if (temp.lowerBound==-1 or temp.lowerBound == LB): ## if -1 then unvisited, if LB some other tile from this same level has visited this tile before but in a different direction, so we need to check
					while(not temp.wallDict["NORTH"]): 	##loop keep going north
						if (temp.lowerBound  == -1):	## unvisited 
							temp.lowerBound = LB
							newList.append(temp)	##add to queue	
						temp=self.array[temp.position[0]-1,c] ## loop to next
					if (temp.lowerBound==-1):		## loop stoped one tile before the last tile , now is checking
						temp.lowerBound=LB
						newList.append(temp)
			if (not tile.wallDict["EAST"]):## check all tiles to the east of current tile
				temp = self.array[r,c+1]
				if (temp.lowerBound==-1 or temp.lowerBound == LB):
					while(not temp.wallDict["EAST"]):
						if (temp.lowerBound  == -1):
							temp.lowerBound = LB
							newList.append(temp)
						temp=self.array[r,temp.position[1]+1]
					if (temp.lowerBound==-1):
						temp.lowerBound=LB
						newList.append(temp)
			if (not tile.wallDict["SOUTH"]):## check all the tiles to the south of the current tile
				temp = self.array[r+1,c]
				if (temp.lowerBound==-1 or temp.lowerBound == LB):
					while(not temp.wallDict["SOUTH"]):
						if (temp.lowerBound  == -1):
							temp.lowerBound = LB
							newList.append(temp)
						temp=self.array[temp.position[0]+1,c]
					if (temp.lowerBound==-1):
						temp.lowerBound=LB
						newList.append(temp)
			if (not tile.wallDict["WEST"]):## check all the tiles to the west
				temp = self.array[r,c-1]
				if (temp.lowerBound==-1 or temp.lowerBound == LB):
					while(not temp.wallDict["WEST"]):
						if (temp.lowerBound  == -1):
							temp.lowerBound = LB
							newList.append(temp)
						temp=self.array[r,temp.position[1]-1]
					if (temp.lowerBound==-1):
						temp.lowerBound=LB
						newList.append(temp)
		self.paintLB(newList,LB+1)## proceed to the next level with new list contains the queue
		
		
	def lowerBoundPreProc(self):
		'''pre-process the board with lower bound heuristics'''

		row,col =self.currentTarget
		self.array[row,col].lowerBound=0
		initList =[]
		for i in xrange(4):
			initList += self.getRay(row,col,i)
		for t in initList:
			t.lowerBound = 1
		self.paintLB(initList,2)
	
	def printLBs(self):
		'''this function displays the board heuristics'''
		
		for i in xrange(self.rows):
			a =""
			for j in xrange(self.cols):
				a+=str(self.array[i,j].lowerBound)
			print (a)
	
	def printRBs(self):
		'''this function displays the board heuristics'''
		
		for i in xrange(self.rows):
			a =""
			for j in xrange(self.cols):
				if (self.array[i,j].reachable>=10):
					a+=" "+str(self.array[i,j].reachable)+" "
				else:
					a+=" "+str(self.array[i,j].reachable)+"  "
			print (a)
		
	
	def CalcReachability(self,firsttime):
		''' calculate reachability 
		
			input boolean firsttime indicate if erase previous information, true = erase
			
			return n s
			
			n: number of tiles can be reached from this target
			
			S :  sum of increase and decrease from a previous state of the board.
				increase decrease in respect of number of moves to reach target, the tile.reachable 
		'''
		
		r,c =self.currentTarget
		
		if(firsttime): ## clean  RB
			for i in xrange(self.rows):
				for j in xrange(self.cols):
					self.array[i,j].reachable=-1
		for i in xrange(self.rows): ## clean visited flag, is only used in paintRB
			for j in xrange(self.cols):		
				self.array[i,j].check =False
		a=[]
		self.array[r,c].reachable =0
		self.array[r,c].check = True
		a.append(self.array[r,c])
		n,s = self.paintRB(a,1)
		
		return n,s
	
	
	
	def shootRay(self,direction,r,c,RB,newList):
	
		direct = ["NORTH","EAST","SOUTH","WEST"]
		pace =[[-1,0],[0,1],[1,0],[0,-1]]
		
		nums=0
		sums=0
		tile = self.array[r,c]
		
		if (not tile.wallDict[direct[direction]] and (tile.wallDict[direct[(direction+2)%4]] or self.getAdjacentTile(tile,(direction+2)%4).robot>0) and (tile.robot==None or tile.robot ==0)):
			temp = self.array[r+pace[direction][0],c+pace[direction][1]] ## one step
#				
			while(not temp.wallDict[direct[direction]] and (temp.robot == None or temp.robot==0)): ## looping
				if (temp.check == False):
					temp.check =True ## calc score
					nums +=1
					if(temp.reachable<RB):
						sums -= 1
					elif (temp.reachable >RB):
						sums+=1
					temp.reachable = RB
					
					tile1 = self.getAdjacentTile(temp,(direction+1)%4)
					tile2 = self.getAdjacentTile(temp,(direction+3)%4)
					#if (tile1.robot>0):
					#	print (tile2.robot)
					if (temp.wallDict[direct[(direction+1)%4]] != temp.wallDict[direct[(direction+3)%4]] or (tile1!=None and tile1.robot!=0) or (tile2!=None and tile2.robot!=0)):
						newList.append(temp)
				temp=self.array[temp.position[0]+pace[direction][0],temp.position[1]+pace[direction][1]]
			if (temp.check == False and (temp.robot == None or temp.robot==0)):## last tile after the loop
				temp.check =True
				nums +=1
				if(temp.reachable<RB):
					sums -= 1
				elif (temp.reachable >RB):
					sums +=1
				temp.reachable = RB
				tile1 = self.getAdjacentTile(temp,(direction+1)%4)
				tile2 = self.getAdjacentTile(temp,(direction+3)%4)
				if (temp.wallDict[direct[(direction+1)%4]] != temp.wallDict[direct[(direction+3)%4]] or (tile1!=None and tile1.robot!=0) or (tile2!=None and tile2.robot!=0)):
					newList.append(temp)
		return nums,sums		
	
	def paintRB(self,tileList,RB):
		'''recursive function to calculate Reachability on each tile, 
		each tile should starte with score -1 only if it was the first time painting
		at the end of the function, if some tile was not visited ,
		that means it is not reachable from the target tile
		thus would also have a score of -1
		
		input arguement should be the a list of tiles  
		'''
		
		nums =0; ## number of tiles can be reached
		sums =0; ## sum of score : +1 for RB decrease from previous state, -1 for RB increase from previous state 
		if (not tileList):
			
			return nums,sums
		newList =[]
		
		for tile in tileList:
			
			r = tile.position[0]
			c = tile.position[1]
			for i in xrange(4):
				n,s =self.shootRay(i,r,c,RB,newList)	
				nums+=n
				sums+=s	
		num1, sum1 = self.paintRB(newList,RB+1)
#		print (nums)
		nums += num1
		sums += sum1
		return nums, sums
	def correctWall(self):
	# this function checks current board is legal, and correct any walls with illegal placement
		r = self.rows
		c = self.cols
		for i in xrange(r):
			for j in xrange(c):
				if (i== 7 and j ==15):
					print self.array[i,j].wallDict
				if(i>0):
					t = self.array[i,j].wallDict["NORTH"] or self.array[i-1,j].wallDict["SOUTH"]
					self.array[i,j].wallDict["NORTH"]=t
					self.array[i-1,j].wallDict["SOUTH"] = t
				else:
					
					self.array[i,j].wallDict["NORTH"]=True
				if (i== 7 and j ==15):
					print self.array[i,j].wallDict
				if(i<r-1):
					t = self.array[i+1,j].wallDict["NORTH"] or self.array[i,j].wallDict["SOUTH"]
					self.array[i+1,j].wallDict["NORTH"]=t
					self.array[i,j].wallDict["SOUTH"] = t
				else:
					self.array[i,j].wallDict["SOUTH"]=True
				if (i== 7 and j ==15):
					print self.array[i,j].wallDict
				if(j>0):
					t = self.array[i,j].wallDict["WEST"] or self.array[i,j-1].wallDict["EAST"]
					self.array[i,j].wallDict["WEST"]=t
					self.array[i,j-1].wallDict["EAST"] =t
				else:
					self.array[i,j].wallDict["WEST"]=True
				if (i== 7 and j ==15):
					print self.array[i,j].wallDict
				if(j<c-1):
					
					t = self.array[i,j+1].wallDict["WEST"] or self.array[i,j].wallDict["EAST"]
					self.array[i,j+1].wallDict["WEST"]=t
					self.array[i,j].wallDict["EAST"] = t
				else:
					self.array[i,j].wallDict["EAST"]=True
				if (i== 7 and j ==15):
					print self.array[i,j].wallDict



############################## RandomBoard Subclass ####################################

			
class RandomBoard(Board):
	''' the random board which initializes the tiles randomly '''
	
	
	def __init__(self, rows, cols):
		Board.__init__(self, rows, cols) # call super constructor
		self.array = self.initializeTiles()
		self.targetPositions = self.initializeTargetPositions()
		self.robotPositions = self.initializeRobotPositions()
		self.correctWall()
	
	def reinitializeTileWithPercentage(self,percent):
		self.array = self.genTileWithCorner(percent)
		self.correctWall()
		self.targetPositions = self.initializeTargetPositions()
		self.setTarget()
		self.lowerBoundPreProc()
		self.robotPositions = self.initializeRobotPositions()
		
	
	def initializeTiles(self):
		''' this method initializes the array of tiles randomly.
			this includes wall placement but not robots or targets '''
		result = np.empty((self.rows, self.cols), dtype=object)
		# for each position on the board, generate a random tile (the wall placement)
		for i in xrange(self.rows):
			for j in xrange(self.cols):
				result[i,j] = self.generateRandomTile((i,j))
		
		return result
	
	def initializeRobotPositionsWithReachability():
		'''this function initialzie robots within the reachable tiles'''
		robotPositions = dict()
		for robot in xrange(4):
			# the while loop ensures that robots have unique positions.
			while(True):
				iCoord = random.randint(0, self.rows-1)
				jCoord = random.randint(0, self.cols-1)
				if (iCoord, jCoord) in robotPositions.values():
					continue # another robot is already at this position so try again
				elif self.array[iCoord, jCoord].target != None:
					continue
				elif self.array[iCoord, jCoord].lowerBound == -1:
					continue
				else:
					robotPositions[robot] = (iCoord, jCoord)
					self.array[iCoord, jCoord].robot = robot
					break # move onto the next robot in the outer for loop
		return robotPositions
		
		
		
	def generateRandomTile(self, position):
		wallDict = dict()
		boolList = [True, False]
		for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
			wallDict[direction] = boolList[random.randint(0,1)]
		return Tile.Tile(position, None, None, wallDict) # return a tile with random walls and None robot/target


	
				


	def initializeTargetPositions(self):
		''' this method places the 17 targets randomly on the board.
			self.array gets updated such that the tiles know when they posses a target.
			A dictionary containing the targets is returned '''
		result = [(random.randint(0,15),random.randint(0,15))]
		print result
		return result
	
	def genTileWithCorner(self,percent):
		''' this method initializes the array of tiles randomly.
			this includes wall placement but not robots or targets 
			only produces corner walls with input probability out of 100'''
		result = np.empty((self.rows, self.cols), dtype=object)
		# for each position on the board, generate a random tile (the wall placement)
		for i in xrange(self.rows):
			for j in xrange(self.cols):
				x = random.randint(0,100)
				if (x < percent):
					result[i,j] = self.getConner((i,j))
				else:
					result[i,j] =Tile.Tile((i,j), None, None, {"NORTH" : False, "EAST" : False,"WEST" : False, "SOUTH":False})
		print 'herer'
				
		
		return result
	

	def getConner(self,position):
		
		a = [{"NORTH" : True, "EAST" : True,"WEST" : False, "SOUTH":False},
		{"NORTH" : True, "EAST" : False,"WEST" : True, "SOUTH":False},
		{"NORTH" : False, "EAST" : False,"WEST" : True, "SOUTH":True},
		{"NORTH" : False, "EAST" : True,"WEST" : False, "SOUTH":True}]
		x = random.randint(0,3)
		return Tile.Tile(position, None, None, a[x])
		

########################### StandardBoard Subclass ##############################


class StandardBoard(Board):
	''' the standard board hard codes the board array to be a built-in one from the game '''


	def __init__(self, rows, cols, inputFileName):
		Board.__init__(self, rows, cols) # call super constructor

		# set the array, robot, and target positions to be empty for now
		self.array = np.empty((self.rows, self.cols), dtype=object)
		self.targetPositions = []
		self.robotPositions = dict()
		
		# now read the board information from the input file
		self.readFromFile(inputFileName)







	def readFromFile(self, inputFileName):
		''' standard board reads an input text file with a board representation to se the board.
			hex numbers 0-f each represent one of the 2^4 different wall configurations. A text file
			consists of 16 lines with a hex number for each of the 16 tiles, followed by the robot and target positions.'''
		lineCount = 0
		with  open(inputFileName, 'r') as file:
			for line in file:
				line = line.strip()
				if lineCount < self.rows:
					self.processArrayLine(line, lineCount)
				elif lineCount < self.rows+4:
					self.processRobotLine(line)
				else:
					self.processTargetLine(line)
				lineCount += 1
		
		

	def processArrayLine(self, line, lineCount):
		''' pass an array line from the input file. This method sets that line's tiles in the np array '''
		for j in xrange(self.cols):
			position = (lineCount, j)
			self.array[lineCount, j] = self.generateTileFromNumber(line[j], position)


	def processRobotLine(self, line):
		''' called on a line from the input board that is giving the location of a robot '''
		for j in xrange(len(line)):
			if line[j] == "=":
				iCoord, jCoord = line[j+1:].split(",")
				robotINT = Board.conversionDict[line[:j]]
				self.robotPositions[robotINT] = (int(iCoord), int(jCoord))
				self.array[iCoord, jCoord].robot = robotINT
			
			
	def processTargetLine(self, line):
		''' called on a line from the input board that is giving the locations of the targets '''
		if line[0] != "T":
			# called on the wrong line
			return
		targetCoords = line[2:].split(" ")
		for coord in targetCoords:
			iCoord, jCoord = coord.split(",")
			self.targetPositions.append((int(iCoord),int(jCoord)))
			self.array[iCoord, jCoord].target = True
		


	def generateTileFromNumber(self, number, positon):
		''' when reading from the txt file, this is called to process a given number.
			Each number corresponds to a wall configuration. A tile with this configuration is returned'''
		
		if number == "0":
			return self.generateTileFromDirections([], positon)
		elif number == "1":
			return self.generateTileFromDirections(["NORTH"], positon)
		elif number == "2":
			return self.generateTileFromDirections(["EAST"], positon)
		elif number == "3":
			return self.generateTileFromDirections(["NORTH", "EAST"], positon)
		elif number == "4":
			return self.generateTileFromDirections(["SOUTH"], positon)
		elif number == "5":
			return self.generateTileFromDirections(["NORTH","SOUTH"], positon)
		elif number == "6":
			return self.generateTileFromDirections(["EAST","SOUTH"], positon)
		elif number == "7":
			return self.generateTileFromDirections(["NORTH", "EAST", "SOUTH"], positon)
		elif number == "8":
			return self.generateTileFromDirections(["WEST"], positon)
		elif number == "9":
			return self.generateTileFromDirections(["WEST", "NORTH"], positon)
		elif number == "a":
			return self.generateTileFromDirections(["WEST","EAST"], positon)
		elif number == "b":
			return self.generateTileFromDirections(["WEST", "NORTH","EAST"], positon)
		elif number == "c":
			return self.generateTileFromDirections(["WEST","SOUTH"], positon)
		elif number == "d":
			return self.generateTileFromDirections(["WEST", "NORTH","SOUTH"], positon)
		elif number == "e":
			return self.generateTileFromDirections(["WEST","SOUTH","EAST"], positon)
		elif number == "f":
			return self.generateTileFromDirections(["WEST", "NORTH","SOUTH","EAST"], positon)
			
		else:
			print("Error no wall configuration for this input number = {}!".format(number))
	
	
	

	def generateTileFromDirections(self, directionsList, position):
		''' pass a list of directions which posses a wall. this method returns a tile object with those wall
			directions set to True in its wallDict '''
		wallDict = dict()
		# first initialize no walls (all False)
		for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
			wallDict[direction] = False
		
		#now for the directions passed to the function, set them to True
		for direction in directionsList:
			wallDict[direction] = True
		
		return Tile.Tile(position, None, False, wallDict) # return a tile with  walls and None robot and False target






	
			
			
