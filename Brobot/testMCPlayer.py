#!/usr/bin/python

import MCPlayer
import Board
import sys, traceback


def testInit():
	''' use a standard board to test a MC player '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = MCPlayer.MCPlayer(rr)
		if rPlayer.board != None:
			return 1
		else:
			return 0
	except:
		print("exception in testInit")
		return 0





def testFindFirstSol():
	''' use a standard board to test a MCPlayer's play method '''
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		mcPlayer = MCPlayer.MCPlayer(rr)
		mcPlayer.setTarget()
		numSamples = 10
		depth = 5
		
		print("robot positions before call to findFirstSol = {0}".format(mcPlayer.board.robotPositions))
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		print("robot positions after call to findFirstSol = {0}".format(mcPlayer.board.robotPositions))
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			print("valid sequence with {} moves!".format(numMoves))
			return 1
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return 0

	except:
		print("exception in testPlay")
		traceback.print_exc(file=sys.stdout)
		return 0






if __name__ == "__main__":

	tests = [testInit, testFindFirstSol]

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