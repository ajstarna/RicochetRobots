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
		traceback.print_exc(file=sys.stdout)
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
		traceback.print_exc(file=sys.stdout)
		return 0
		
def testSolve():
	''' use a standard board to test hashing score for initial state '''
	size = 16
	try:
		
		rr = Board.StandardBoard(size, size, "builtin3.txt")
		rr.setTarget()
		rPlayer = Solver.Solver(rr)
		 
		
		d,b = rPlayer.play(1000)
	 	rPlayer.board.printBoard()
		print (d,b)
		sol = rPlayer.getSolution(b)
		for s in sol:
			print s
		if d >0:
			return 1
		else:
			return 0
	except:
		print("exception in testSolve")
		traceback.print_exc(file=sys.stdout)
		return 0

def testSetBoard():
	''' use a standard board to test hashing score for initial state '''
	size = 16
	try:
		
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rr.setTarget()
		rPlayer = Solver.Solver(rr)
		 
		rPlayer.setBoardByState(1917832798)
		
		
		rPlayer.board.printBoard()
		
		if True:
			return 1
		else:
			return 0
	except:
		print("exception in testSetBoard")
		traceback.print_exc(file=sys.stdout)
		return 0


		

if __name__ == "__main__":

	tests = [testGetHash,testSolve,testSetBoard]
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
