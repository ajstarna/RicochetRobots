
#!/usr/bin/python
import Solver
import sys, traceback
import Board


def testGetHash():
	''' use a standard board to test hash function '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		
		rPlayer = Solver.Solver(rr)
		
		
		if pow(2,rPlayer.getHash()) == 256:
			return 1
		else:
			return 0
	except:
		print("exception in testGetHash")
		return 0


def testInitState():
	''' use a standard board to test hashing score for initial state '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		
		rPlayer = Solver.Solver(rr)
		rPlayer.play(1,[],0)
		
		if pow(2,rPlayer.getHash()) == 256:
			return 1
		else:
			return 0
	except:
		print("exception in testInitState")
		return 0
def testSolve():
	''' use a standard board to test hashing score for initial state '''
	size = 16
	try:
		
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		
		rPlayer = Solver.Solver(rr)
		print ('d')
		d,b = rPlayer.play(1000)
		
		if d >0:
			return 1
		else:
			return 0
	except:
		print("exception in testSolve")
		return 0

if __name__ == "__main__":

	tests = [testGetHash,testInitState,testSolve]
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
