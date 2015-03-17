#!/usr/bin/python


''' this file contains unit tests for the clobber board. To test model functionaility '''

import Board
import Move
import sys
import traceback



def testInitRandom():
	''' test the basic initialization of a Board object '''

	size = 16
	try:
		rr = Board.RandomBoard(size, size)
		if rr.array.size != size*size:
			return 0
		if rr.rows != size or rr.cols != size:
			return 0
		if len(rr.robotPositions) != 4:
			return 0
		if len(rr.targetPositions) != 17:
			return 0

		return 1

	except:
		print("exception in testInitRandom")
		traceback.print_exc(file=sys.stdout)
		return 0


def testRobotPlacement():
	''' test that the four robots are placed on the board in distinct spots. Uses a random board '''
	size = 16
	try:
		rr = Board.RandomBoard(size,size)
		positions = rr.robotPositions
		for i in xrange(4):
			position = positions[i]
			if positions.values().count(position) > 1:
				return 0
			if position[0] < 0 or position[0] >= size or position[1] < 0 or position[1] >= size:
				return 0

		return 1
	except:
		print("exception in testRobotPlacement!")
		traceback.print_exc(file=sys.stdout)
		return 0


def testInitStandard():
	''' test the basic initialization of a Board object '''

	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		if rr.array.size != size*size:
			return 0
		if rr.rows != size or rr.cols != size:
			return 0
		if len(rr.robotPositions) != 4:
			return 0
		if rr.targetPositions == []:
			return 0

		return 1

	except:
		print("exception in testInitStandard")
		traceback.print_exc(file=sys.stdout)
		return 0


def testPrintBoard():
	size =16
	rr = Board.StandardBoard(size,size, "builtin1.txt")
	rr.printBoard()
	return 1



def testLowerBounds():
	size =16
	rr = Board.StandardBoard(size,size, "builtin1.txt")
	rr.lowerBoundPreProc(rr.array[3,4])
	rr.printLBs()
	return 1

def testReachability():
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		n,s = rr.CalcReachability(3,4,True)
		
		print ("number of tiles can be reached :" + str( n))
		return 1
		
	except:
		print("exception in testMakeMove")
		traceback.print_exc(file=sys.stdout)
		return 0

def testMakeMove():
	''' test making a move in the board '''
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		move = Move.Move(Board.BLUE, "SOUTH") # create the move object
		initalPosition = rr.robotPositions[Board.BLUE]
		if initalPosition != (5,1):
			return 0 # not what we excepted from builtin1.txt
		
		rr.makeMove(move) # now make the move
		
		if rr.robotPositions[Board.BLUE] != (12,1):
			return 0 # not what we excepted from builtin1.txt
		
		return 1

	except:
		print("exception in testMakeMove")
		traceback.print_exc(file=sys.stdout)
		return 0




if __name__ == "__main__":

	tests = [testInitRandom, testRobotPlacement, testInitStandard, testPrintBoard, testLowerBounds, testMakeMove,testReachability]

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










	
