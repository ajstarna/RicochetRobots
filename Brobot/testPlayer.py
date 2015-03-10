import Player
import Board


def testInitRandom():
	''' use a standard board to test a random player '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = Player.RandomPlayer(rr)
		if rPlayer.board != None:
			return 1
		else:
			return 0
	except:
		print("exception in testInitRandom")
		return 0



def testShowBoard():
	''' use a standard board to test a random player's showBoard method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = Player.RandomPlayer(rr)
		rPlayer.showBoard()
		return 1

	except:
		print("exception in testShowBoard")
		return 0


if __name__ == "__main__":

	tests = [testInitRandom, testShowBoard]

	totalTestsRan = 0
	passedTests = 0
	for test in tests:
		totalTestsRan += 1
		result = test()
		passedTests += result
		if result:
			print("Passed: " + str(test))
		else:
			print("Failed: " + str(test))

	print("Passed {}/{} tests!".format(passedTests, totalTestsRan))