import Board


class Player:
	''' this player abstract class contains a Board and has methods for playing the game.
		it is the subclasses' job to implement how the game is played '''



	def __init__(self, board):
		self.board = board


	def showBoard(self):
		self.board.printBoard()