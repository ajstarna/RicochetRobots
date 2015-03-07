class Target:
	''' a target on the board contains a colour and a position. 
		the shape of the target (triangle, circle, etc.) should not matter so is not included in the implementation '''
	def __init__(self, colour, position):
		self.colour = colour
		self.position = position