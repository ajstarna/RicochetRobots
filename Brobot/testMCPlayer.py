#!/usr/bin/python

import Player
import Board
import sys, traceback


def testInit():
	''' use a standard board to test a MC player '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = Player.MCPlayer(rr)
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
		mcPlayer = Player.MCPlayer(rr)
		mcPlayer.setTarget()
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit()
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return 1
		else:
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