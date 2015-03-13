import numpy as np
import Tile
import random

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



	def initializeTiles(self):
		''' this method initializes the array of tiles randomly.
			this includes wall placement but not robots or targets '''
		raise NotImplementedError("Please implement this method")

	def initializeTargetPositions(self):
		''' this method places the 17 targets on the board.
			consider an abstract method '''
		raise NotImplementedError("Please implement this method")
	
	
	def setCurrentTarget(self):
		''' this method will pick a random target from the target list and make that the currentTarget for the game '''
		self.currentTarget = random.sample(self.targetPositions, 1)
		self.targetPositions.remove(self.currentTarget)
	
		
		
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




	def makeMove(self, move):
		''' given a move, make it on the board (so move the colour in the direction and update the array) '''
		startPosition = self.robotPositions[move.colour] # initalize the endPosition to be the starting position
		# now see how far the robot can move in the direction
		currentTile = self.array[startPosition]
		while True:
			if currentTile.wallDict[direction]:
				# there is a wall in the direction we need to move, so final spot
				break
			# since an edge tile will always have a wall, if we made it to here then we know we can find the adjacent tile
			adjacentTile = self.getAdjacentTile(currentTile, direction)
			if adjacentTile.robot != None:
				# there is a robot blocking us, so final spot
				break

			# no wall or robot in the way, so move the robot onto the adjacent tile
			adjacentTile.robot = currentTile.robot
			currentTile.robot = None
			self.robotPositions[colour] = adjacentTile.position
			currentTile = adjacentTile

		# the currentTile is the ending position
		
		
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
		if (direction ==0 && r > 0): #NORTH
			
			currentTile = self.array[r-1,c]
			while (!currentTile.wallDict["NORTH"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r-1,c]
			ray.append(currentTile)
		elif (direction == 1 && c<self.cols): # EAST
			currentTile = self.array[r,c+1]
			while (!currentTile.wallDict["EAST"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r,c+1]	
			ray.append(currentTile)
		elif (direction == 2 && r<self.rows): # SOUTH
			currentTile = self.array[r+1,c]
			while (!currentTile.wallDict["SOUTH"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r+1,c]
			ray.append(currentTile)	
		elif (direction == 3 && c>0): # WEST- 
			currentTile = self.array[r,c-1]
			while (!currentTile.wallDict["EAST"]):
			 	ray.append(currentTile)
			 	currentTile = self.array[r,c-1]	
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
		if (!tileList):
			return
		newList =[]
		for tile in tileList:
			for d in xrange(4):
			r = tile.position[0]
			c = tile.position[1]
			if (!tile.wallDict["NORTH"]):
				temp = self.array[r-1,c]
				if (temp.lowerBound==-1 || temp.lowerBound == LB):
					while(!temp.wallDict["NORTH"]):
						if (!temp.lowerBoard  == -1):
							temp.lowerBoard = LB
							newList.append(temp)
						temp=self.array[temp.position[0]-1,c]
			if (!tile.wallDict["EAST"]):
				temp = self.array[r,c+1]
				if (temp.lowerBound==-1 || temp.lowerBound == LB):
					while(!temp.wallDict["EAST"]):
						if (!temp.lowerBoard  == -1):
							temp.lowerBoard = LB
							newList.append(temp)
						temp=self.array[r,temp.position[1]+1]
			if (!tile.wallDict["SOUTH"]):
				temp = self.array[r+1,c]
				if (temp.lowerBound==-1 || temp.lowerBound == LB):
					while(!temp.wallDict["SOUTH"]):
						if (!temp.lowerBoard  == -1):
							temp.lowerBoard = LB
							newList.append(temp)
						temp=self.array[temp.position[0]+1,c]
			if (!tile.wallDict["WEST"]):
				temp = self.array[r,c-1]
				if (temp.lowerBound==-1 || temp.lowerBound == LB):
					while(!temp.wallDict["WEST"]):
						if (!temp.lowerBoard  == -1):
							temp.lowerBoard = LB
							newList.append(temp)
						temp=self.array[r,temp.position[1]-1]
		paintLB(newList,LB+1)
		
		
	def lowerBoundPreProc(self,targetTile):
		'''pre-process the board with lower bound heuristics'''
		targetTile.lowerBound=0;
		row =targetTile.position[0]
		col =targetTile.position[1]
		initList =[]
		for i in xrange(4):
			initList + getRay(row,col,i)
		paintLB(initList,1)
		
		
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
				result[i,j] = self.generateRandomTile()
		return result
	
	
	def generateRandomTile(self):
		wallDict = dict()
		boolList = [True, False]
		for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
			wallDict[direction] = boolList[random.randint(0,1)]
		return Tile.Tile(None, None, wallDict) # return a tile with random walls and None robot/target





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
				self.robotPositions[robotINT] = (iCoord, jCoord)
				self.array[iCoord, jCoord].robot = robotINT
			
			
	def processTargetLine(self, line):
		''' called on a line from the input board that is giving the locations of the targets '''
		if line[0] != "T":
			# called on the wrong line
			return
		targetCoords = line[2:].split(" ")
		for coord in targetCoords:
			iCoord, jCoord = coord.split(",")
			self.targetPositions.append((iCoord,jCoord))
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






	
			
			
