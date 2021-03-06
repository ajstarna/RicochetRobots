#!/usr/bin/python

import MCPlayer
import Board
import sys, traceback
import time

def testInit(name):
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
		print("exception in {}".format(name))
		return 0





def testFindFirstSol(name):
	''' use a standard board to test a MCPlayer's play method '''
	size = 16
	fileName = "builtin1.txt"
	try:
		rr = Board.StandardBoard(size, size, fileName)
		mcPlayer = MCPlayer.MCPlayer(rr)
		mcPlayer.setTarget()
		numSamples = 10
		depth = 5
		
		#print("robot positions before call to findFirstSol = {0}".format(mcPlayer.board.robotPositions))
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		#print("robot positions after call to findFirstSol = {0}".format(mcPlayer.board.robotPositions))
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			print("valid sequence with {} moves!".format(numMoves))
			return 1
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return 0

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0



def testPlay(name):
	''' use a standard board to test a MCPlayer's play method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		mcPlayer = MCPlayer.MCPlayer(rr)
		mcPlayer.setTarget()
		numSamples = 10
		depth = 3
		
		
		
		moveSequence, numMoves = mcPlayer.play(2, numSamples, depth) # let it search for 3 seconds
		
		if numMoves < 15:
			mcPlayer.printMoveSequence(moveSequence)

		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			print("valid sequence with {0} moves!".format(numMoves))
			return 1
		elif numMoves == 0:
			print("no sequence found in time limit!")
			return 1
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0
def testRandPlay(name):
	''' use a Random board to test a MCPlayer's play method '''
	size = 16
	try:
		
		rr = Board.RandomBoard(size, size)
		
		rr.reinitializeTileWithPercentage(30)
		mcPlayer = MCPlayer.PNGSPlayer(rr)
		
		
		numSamples = 20
		depth =20
		
		
		rr.printBoard()
		moveSequence, numMoves = mcPlayer.play(10,numSamples,depth) # let it search for 3 seconds
		#change, newSequence = mcPlayer.pngs(moveSequence, numSamples, depth)
		#rr.printBoard()
		
		if numMoves < 15:
			mcPlayer.printMoveSequence(moveSequence)

		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			print("valid sequence with {0} moves!".format(numMoves))
			return 1
		elif numMoves == 0:
			print("no sequence found in time limit!")
			return 1
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0

def testRandPlay2(name):
	''' use a Random board to test a MCPlayer's play method '''
	size = 16
	try:
		re =0
		for i in xrange (50):
			rr = Board.RandomBoard(size, size)
		
			rr.reinitializeTileWithPercentage(5)
			mcPlayer = MCPlayer.PNGSPlayer(rr)
		
		
			numSamples = 20
			depth =20
		
		
			#rr.printBoard()
			moveSequence, numMoves = mcPlayer.play(10,numSamples,depth) # let it search for 3 seconds
		#change, newSequence = mcPlayer.pngs(moveSequence, numSamples, depth)
		#rr.printBoard()
		
			if numMoves > 50:
				#mcPlayer.printMoveSequence(moveSequence)
				print numMoves

			if rr.validateMoveSequence(moveSequence):
				re+=1
		print re
		return 1

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0

def testPNGS(name):
	''' use a standard board to test pngs method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		mcPlayer = MCPlayer.PNGSPlayer(rr)
		mcPlayer.setTarget()
		
		
		moveSequence = [1, 6,7, 4,2,0,2,10,0,3]
		mcPlayer.printMoveSequence(moveSequence)
		print(moveSequence)
		numSamples = 0
		depth = 0
		
		change, newSequence = mcPlayer.pngs(moveSequence, numSamples, depth)
		numMoves = len(newSequence)
		

		if not change:
			print("did not improve the sequence")
			return 0

		if rr.validateMoveSequence(newSequence):
			# if the move sequence
			print("valid new sequence with {0} moves!".format(numMoves))
			
			mcPlayer.printMoveSequence(newSequence)
			print(newSequence)
			return 1
		else:
			print("Invalid new sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0


def testPruning(name):
	''' use a standard board to test a MC player '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		rPlayer = MCPlayer.PNGSPlayer(rr)
		rPlayer.setTarget()
		seq = [1, 4, 2, 5, 0, 2,10, 0, 3]
		newseq = rPlayer.pruneSequence(seq)
		print newseq
		if len(newseq)== 8:
			return 1
		else:
			return 0
	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0


def testHardest(name):
	''' use athe hardest board to test a PNGSPlayer's first sol method '''
	size = 16
	try:
		rr = Board.StandardBoard(size, size, "builtin1.txt")
		
		reachableWeight = 4
		LBWeight = 1
		totalReachableWeight = 3
		
		pngsPlayer = MCPlayer.PNGSPlayer(rr,  reachableWeight, LBWeight, totalReachableWeight)
		pngsPlayer.setTarget()
		
		numSamples = 10
		depth = 1

		
		tStart = time.clock()
		#moveSequence, numMoves = pngsPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		moveSequence, numMoves = pngsPlayer.play(1, numSamples, depth)
		print("time total = {0}".format(time.clock()-tStart))
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			
			print("valid move sequence with {0} moves!".format(numMoves))
			
			#pngsPlayer.printMoveSequence(moveSequence)
			return 1
		else:
			print("Invalid move sequence with {0} moves!".format(numMoves))
			return 0

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0




if __name__ == "__main__":

	#tests = [testInit, testFindFirstSol, testPlay, testPNGS]
	#tests = [testPNGS,testPruning]
	#tests = [testHardest]
	tests =[testRandPlay2]
	totalTestsRan = 0
	passedTests = 0
	for test in tests:
		totalTestsRan += 1
		result = test(str(test))
		passedTests += result
		if result:
			print("Passed: " + str(test))
		else:
			print("Failed: " + str(test))

	print("Passed {}/{} tests!".format(passedTests, totalTestsRan))








