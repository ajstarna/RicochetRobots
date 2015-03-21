#!/usr/bin/python

import Player
import Board
import sys, traceback


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



def testFindFirstSol():
	''' use a standard board to test a RandomPlayer's play method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = Player.RandomPlayer(rr)
		rPlayer.setTarget()
		moveSequence, numMoves, stateSequence = rPlayer.findFirstSolutionNoTimeLimit()
		
		if (not rr.correctRobotTiles()):
			print("Incorrect robot posititions before validations")
		
		if rr.validateMoveSequence(moveSequence, stateSequence):
			# if the move sequence
			print("valid sequence with {0} moves!".format(numMoves))
			return 1
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in testFindFirstSol")
		traceback.print_exc(file=sys.stdout)
		return 0


def testPlay():
	''' use a standard board to test a RandomPlayer's play method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = Player.RandomPlayer(rr)
		rPlayer.setTarget()
		moveSequence, numMoves = rPlayer.play(0.1) # let it search for 3 seconds
		answer = rr.validateMoveSequence(moveSequence)
		print("first validate = {0}".format(answer))
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return 1
		elif numMoves == 0:
			#print("no sequence found in time limit!")
			return 1
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in testPlay")
		traceback.print_exc(file=sys.stdout)
		return 0




if __name__ == "__main__":

	#tests = [testInitRandom, testShowBoard, testFindFirstSol, testPlay]
	tests = [testFindFirstSol]
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