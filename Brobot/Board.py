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


	def makeMoveByInt(self, moveInt):
		''' this method will take an integer and make the move that that intege corresponds to.
			in this way, we can store moves as just an integer and convert them as needed.
			board will contain an AllMoves object where the move is grabbed from '''
		move = self.allMoves.getMoveAtIndex(moveInt)
		self.makeMove(move)


	def makeMove(self, move):
		''' given a move, make it on the board (so move the colour in the direction and update the array) '''

		
		startPosition = self.robotPositions[move.colour] # initalize the endPosition to be the starting position
		
		#print("Start position = {}".format(startPosition))
		# now see how far the robot can move in the direction
		currentTile = self.array[startPosition]
		while True:
			if currentTile.wallDict[move.direction]:
				# there is a wall in the direction we need to move, so final spot
				break
			# since an edge tile will always have a wall, if we made it to here then we know we can find the adjacent tile
			adjacentTile = self.getAdjacentTile(currentTile, move.direction)
			if adjacentTile.robot != None:
				# there is a robot blocking us, so final spot
				break

			# no wall or robot in the way, so move the robot onto the adjacent tile
			adjacentTile.robot = currentTile.robot
			currentTile.robot = None
			self.robotPositions[move.colour] = adjacentTile.position
			currentTile = adjacentTile

		# the currentTile is the ending position
		


	
		
	def getAdjacentTile(self, tile, direction):
		''' given a tile and a direction, this returns the tile adjacent in that direction.
			return None if an edge '''
		i, j = tile.position
		if direction == "NORTH":
			i -= 1
		elif direction == "SOUTH":
			i += 1
		elif direction == "EAST":
			j += 1
		elif direction == "WEST":
			j -= 1

		if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
			# out of bounds
			return None
			
		return self.array[i,j]



	def endState(self):
		''' returns boolean of whether the board is in an end state (i.e. is the right robot at the target '''
		try:
			return self.currentTarget == self.robotPositions[Board.BLUE] #we assume blue is always the target robot
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
		
		#print("original position = {0}".format(resetPositions))
		#print("states[0] = {0}".format(states[0]))
		
		
		for i in sequence:
			
			
			'''if not self.correctRobotTiles():
				print("previous states at i-1 = {2}! {0}, {1}".format(states[i-1], previousState, i-1))
				print("previous move = {}".format(self.allMoves.getMoveAtIndex(sequence[i-1])))
				print("states are different at i = {2}! {0}, {1}".format(states[i], self.robotPositions, i))
				return False
			
			#if states[i] != self.robotPositions:
				print("previous states at i-1 = {2}! {0}, {1}".format(states[i-1], previousState, i-1))
				print("previous move = {}".format(self.allMoves.getMoveAtIndex(sequence[i-1])))
				print("states are different at i = {2}! {0}, {1}".format(states[i], self.robotPositions, i))
				return False
				
			#previousState = deepcopy(self.robotPositions)
			'''
			#print(i)
			self.makeMoveByInt(i)

		

		valid = self.endState()
		#print("robot positions after making moves in validateMoveSequence = {0}".format(self.robotPositions))
		self.resetRobots(resetPositions)
		return valid



	def correctRobotTiles(self):
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
		
		
	def lowerBoundPreProc(self,targetTile):
		'''pre-process the board with lower bound heuristics'''
		targetTile.lowerBound=0;
		row =targetTile.position[0]
		col =targetTile.position[1]
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
		
	
	def CalcReachability(self,r,c,firsttime):
		
		if(firsttime): ## clean  RB
			for i in xrange(self.rows):
				for j in xrange(self.cols):
					self.array[i,j].reachable=-1
		for i in xrange(self.rows): ## clean visited flag, is only used in paintRB
			for j in xrange(self.cols):		
				self.array[i,j].check =False
		a=[]
		a.append(self.array[r,c])
		n,s = self.paintRB(a,1)
		
		return n,s
	
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
			if (not tile.wallDict["NORTH"] and tile.wallDict["SOUTH"]):## north direction, north no wall  south wall
				temp = self.array[r-1,c] ## one step north
#				if (temp.check==False or temp.reachable == RB): ## not visited ? or is visited by current level
				while(not temp.wallDict["NORTH"]): ## looping to the north
					if (temp.check == False):
						temp.check =True ## calc score
						nums +=1
						if(temp.reachable<RB):
							sums -= 1
						elif (temp.reachable >RB):
							sums+=1
						temp.reachable = RB
						if (temp.wallDict["EAST"] != temp.wallDict["WEST"]):
							newList.append(temp)
					temp=self.array[temp.position[0]-1,c]
				if (temp.check == False):## last tile after the loop
					temp.check =True
					nums +=1
					if(temp.reachable<RB):
						sums -= 1
					elif (temp.reachable >RB):
						sums +=1
					temp.reachable = RB
					if (temp.wallDict["EAST"] != temp.wallDict["WEST"]):
						newList.append(temp)		
			if (not tile.wallDict["EAST"] and tile.wallDict["WEST"]): ### same for the east
				temp = self.array[r,c+1]
#				if (temp.check==False or temp.reachable == RB):
				while(not temp.wallDict["EAST"]):
					if (temp.check == False):
						temp.check =True
						nums +=1
						if(temp.reachable<RB):
							sums -= 1
						elif (temp.reachable >RB):
							sums +=1
						temp.reachable = RB
						if (temp.wallDict["NORTH"] != temp.wallDict["SOUTH"]):
							newList.append(temp)
					temp=self.array[r,temp.position[1]+1]
				if (temp.check == False):
					temp.check =True
					nums +=1
					if(temp.reachable<RB):
						sums -= 1
					elif (temp.reachable >RB):
						sums +=1
					temp.reachable = RB
					if (temp.wallDict["NORTH"] != temp.wallDict["SOUTH"]):
						newList.append(temp)
						
			if (not tile.wallDict["SOUTH"] and tile.wallDict["NORTH"]):## south
				temp = self.array[r+1,c]
#				if (temp.check==False or temp.reachable == RB):
				while(not temp.wallDict["SOUTH"]):
					if (temp.check == False):
						temp.check =True
						nums +=1
						if(temp.reachable<RB):
							sums -= 1
						elif (temp.reachable >RB):
							sums +=1
						temp.reachable = RB
						if (temp.wallDict["EAST"] != temp.wallDict["WEST"]):
							newList.append(temp)
					temp=self.array[temp.position[0]+1,c]
				if (temp.check == False):
					temp.check =True
					nums +=1
					if(temp.reachable<RB):
						sums -= 1
					elif (temp.reachable >RB):
						sums +=1
					temp.reachable = RB
					if (temp.wallDict["EAST"] != temp.wallDict["WEST"]):
						newList.append(temp)	
			if (not tile.wallDict["WEST"] and tile.wallDict["EAST"]): ## west
				temp = self.array[r,c-1]
#				if (temp.check==False or temp.reachable == RB):
				while(not temp.wallDict["WEST"]):
					if (temp.check == False):
						temp.check =True
						nums +=1
						if(temp.reachable<RB):
						
							sums -= 1
						elif (temp.reachable >RB):
							sums +=1
						temp.reachable = RB
						if (temp.wallDict["NORTH"] != temp.wallDict["SOUTH"]):
							newList.append(temp)
					temp=self.array[r,temp.position[1]-1]
				if (temp.check == False):
					temp.check =True
					nums +=1
					if(temp.reachable<RB):
						sums -= 1
					elif (temp.reachable >RB):
						sums +=1
					temp.reachable = RB
					if (temp.wallDict["NORTH"] != temp.wallDict["SOUTH"] ):
						newList.append(temp)	
#		print ("new list size :" + str(len(newList)))				
		num1, sum1 = self.paintRB(newList,RB+1)
#		print (nums)
		nums += num1
		sums += sum1
		return nums, sums
############################## RandomBoard Subclass ####################################

			
class RandomBoard(Board):
	''' the random board which initializes the tiles randomly '''
	
	
	def __init__(self, rows, cols):
		Board.__init__(self, rows, cols) # call super constructor
		self.array = self.initializeTiles()
		self.targetPositions = self.initializeTargetPositions()
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
		result = {}
		return result
	




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






	
			
			
