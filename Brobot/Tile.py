
class Tile:
	def __init__(self, position, robot, target, wallDict):
		self.position = position # a tuple of (row,col)
		self.robot = robot # None if no robot, otherwise the int corresponding to a robot colour
		self.target = target # a boolean value for now
		self.wallDict = wallDict # a dictionary; for example: wallDict["NORTH"] == True/False
		self.lowerBound = -1 # the lower bound heuristics, initialized to -1 , after math, -1 means unreachable

	def __str__(self):
		return "Tile with: position = {0}, robot = {1}, target = {2}".format(self.position, self.robot, self.target)