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
		
	def printboard(self):
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
					
					if (self.array[i,j].target != None):
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
	



class StandardBoard(Board):
	''' the standard board hard codes the board array to be a built-in one from the game '''


	def __init__(self, rows, cols):
		Board.__init__(self, rows, cols) # call super constructor
		self.array = self.initializeTiles()
		self.targetPositions = self.initializeTargetPositions()
		self.robotPositions = self.initializeRobotPositions()

	def initializeTiles(self):
		''' this method initializes the array of tiles to match a standard board.
			this includes wall placement but not robots or targets '''
		result = np.empty((self.rows, self.cols), dtype=object)
		for i in xrange(self.rows):
			for j in xrange(self.cols):
				# relatively few of the tiles have wall, so hard-code these as special cases
				if (i,j) == (0,5):
					result[i,j] = self.generateTileFromDirections(["EAST"])
				else:
					result[i,j] = self.generateTileFromDirections([]) # default is no walls
					
		return result


	def generateTileFromDirections(self, directionsList):
		wallDict = dict()
		# first initialize no walls (all False)
		for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
			wallDict[direction] = False
		
		#now for the directions passed to the function, set them to True
		for direction in directionsList:
			wallDict[direction] = True
		
		return Tile.Tile(None, None, wallDict) # return a tile with random walls and None robot/target


	def initializeTargetPositions(self):
		return {}




	
			
			
