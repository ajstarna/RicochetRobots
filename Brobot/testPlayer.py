import Player
import Board


def testInitRandom():
	''' use a standard board to test a random player '''
	size = 16
	rr = Board.StandardBoard(size, size, "builtin1.txt")
	rPlayer = Player.RandomPlayer(rr)
	rPlayer.showBoard()

	return 1




if __name__ == "__main__":

	tests = [testInitRandom]

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