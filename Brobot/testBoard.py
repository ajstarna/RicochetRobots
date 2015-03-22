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
	rr.setTarget()
	rr.lowerBoundPreProc()
	rr.printLBs()
	return 1

def testReachability():
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		rr.setTarget()
		
		n,s = rr.CalcReachability(True)
		rr.printRBs()
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
		move = Move.Move(Board.Board.BLUE, "SOUTH") # create the move object
		initalPosition = rr.robotPositions[Board.Board.BLUE]
		if initalPosition != (5,1):
			print("initial position incorrect")
			return 0 # not what we excepted from builtin1.txt
		
		rr.makeMove(move) # now make the move
		
		if rr.robotPositions[Board.Board.BLUE] != (12,1):
			print("final position incorrect")
			return 0 # not what we excepted from builtin1.txt

		return 1

	except:
		print("exception in testMakeMove")
		traceback.print_exc(file=sys.stdout)
		return 0




def testEndState():
	''' make the necessary moves from builtin2.txt to get to an endstate then see if the board can recognize this '''
	size = 16
	fileName = "builtin2.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		# set the current Target for the game
		rr.setTarget()
		
		move1 = Move.Move(Board.Board.GREEN, "EAST")
		move2 = Move.Move(Board.Board.BLUE, "NORTH")
		move3 = Move.Move(Board.Board.BLUE, "WEST") # create the move object
		
		rr.makeMove(move1) # now make the move
		rr.makeMove(move2) # now make the move
		rr.makeMove(move3) # now make the move
		
		if rr.endState() == True:
			return 1
		else:
			return 0

	except:
		print("exception in testEndState")
		traceback.print_exc(file=sys.stdout)
		return 0


def testResetRobots():
	''' make a couple moves then reset the robots using resetRobots method '''
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		
		reset = rr.robotPositions
		
		move1 = Move.Move(Board.Board.GREEN, "EAST")
		move2 = Move.Move(Board.Board.BLUE, "NORTH")
		move3 = Move.Move(Board.Board.BLUE, "WEST") # create the move object
		
		rr.makeMove(move1) # now make the move
		rr.makeMove(move2) # now make the move
		rr.makeMove(move3) # now make the move
	
		rr.resetRobots(reset)
	
		# test that the robot dict got reset
		if rr.robotPositions != reset:
			return 0

		# now test that the tile make sense
		for i in xrange(size):
			for j in xrange(size):
				tile = rr.array[i,j]
				if (i,j) in rr.robotPositions.values() and tile.robot == None:
					# the dictionary says this tile should have a robot but it doesn't
					return 0
				elif (not (i,j) in rr.robotPositions.values()) and tile.robot != None:
					# the dictionary says this tile should not have a robot but it does
					return 0


		return 1
		
	except:
		print("exception in testEndState")
		traceback.print_exc(file=sys.stdout)
		return 0




def testCopyBoard():
	''' make the necessary moves from builtin2.txt to get to an endstate then see if the board can recognize this '''
	size = 16
	fileName = "builtin2.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		# set the current Target for the game
		rr.setTarget()
		
		move1 = Move.Move(Board.Board.GREEN, "EAST")
		move2 = Move.Move(Board.Board.BLUE, "NORTH")
		move3 = Move.Move(Board.Board.BLUE, "WEST") # create the move object
		
		rr.makeMove(move1) # now make the move
		rr.makeMove(move2) # now make the move
		rr.makeMove(move3) # now make the move
		
		if rr.endState() == True:
			return 1
		else:
			return 0

	except:
		print("exception in testEndState")
		traceback.print_exc(file=sys.stdout)
		return 0




if __name__ == "__main__":


	tests = [testInitRandom, testRobotPlacement, testInitStandard, testPrintBoard, testLowerBounds, testMakeMove, testEndState, testResetRobots,testReachability]


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










	
