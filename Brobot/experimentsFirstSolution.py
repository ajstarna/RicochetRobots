#!/usr/bin/python

''' this file contains functions for experimenting with the different players and for running many trials and averaging results '''

from Player import RandomPlayer
from MCPlayer import MCPlayer, PNGSPlayer, GreedyPlayer
import Board
import sys, traceback
import time

def runRandomPlayerFirstSol(fileName, size, numSamples, depth):
	# numSamples and depth are useless here, just makes it more convenient to call an arbitrary function
	try:
		rr = Board.StandardBoard(size, size, fileName)
		rPlayer = RandomPlayer(rr)
		rPlayer.setTarget()
		moveSequence, numMoves = rPlayer.findFirstSolutionNoTimeLimit()
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {0} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {0} moves!".format(numMoves))
			return None

	except:
		print("exception in runRandomPlayerFirstSol")
		traceback.print_exc(file=sys.stdout)
		return None


def runMCPlayerFirstSol(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		
		reachableWeight = 4
		LBWeight = 1
		totalReachableWeight = 3
		
		mcPlayer = MCPlayer(rr, reachableWeight, LBWeight, totalReachableWeight)
		mcPlayer.setTarget()
		
		moveSequence, numMoves = mcPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runMCPlayerFirstSolution")
		traceback.print_exc(file=sys.stdout)
		return None

def runPNGSPlayerFirstSol(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		
		reachableWeight = 4
		LBWeight = 1
		totalReachableWeight = 3
		
		pngsPlayer = PNGSPlayer(rr, reachableWeight, LBWeight, totalReachableWeight)

		pngsPlayer.setTarget()
		
		moveSequence, numMoves, numMovesBeforePNGS, findTime, pngsTime = pngsPlayer.findFirstSolutionNoTimeLimit(numSamples, depth)
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves, numMovesBeforePNGS, findTime, pngsTime
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runPNGSPlayerFirstSolution")
		traceback.print_exc(file=sys.stdout)
		return None


def runGreedyPlayerFirstSol(fileName, size, numSamples, depth):

	try:
		rr = Board.StandardBoard(size, size, fileName)
		
		reachableWeight = 4
		LBWeight = 1
		totalReachableWeight = 3
		
		greedyPlayer = GreedyPlayer(rr, reachableWeight, LBWeight, totalReachableWeight)

		greedyPlayer.setTarget()
		
		moveSequence, numMoves, numMovesBeforePNGS, findTime, pngsTime = greedyPlayer.findFirstSolutionNoTimeLimit()
		
		if rr.validateMoveSequence(moveSequence):
			# if the move sequence
			#print("valid sequence with {} moves!".format(numMoves))
			return numMoves, numMovesBeforePNGS, findTime, pngsTime
		else:
			print("Invalid sequence with {} moves!".format(numMoves))
			return None

	except:
		print("exception in runGreedyPlayerFirstSolution")
		traceback.print_exc(file=sys.stdout)
		return None


def playMultiplePNGSGames(function, numGames, fileName, size, numSamples, depth):
	totalPNGSMoves = 0
	totalFindMoves = 0
	results = []
	totalFindTime = 0
	totalPNGSTime = 0
	for i in xrange(numGames):
		print("startGame {0}".format(i))
		numMoves, numMovesBeforePNGS, findTime, pngsTime = function(fileName, size, numSamples, depth)
		totalFindTime += findTime
		totalPNGSTime += pngsTime
		if numMoves == None:
			print("Problem in function {0}".format(function))
			sys.exit(-1)
		else:
			results.append((numMoves, numMovesBeforePNGS, findTime, pngsTime))
			totalPNGSMoves += numMoves
			totalFindMoves += numMovesBeforePNGS
	return totalPNGSMoves/float(numGames), totalFindMoves/float(numGames), totalFindTime/float(numGames), totalPNGSTime/float(numGames), results



def playMultipleGames(function, numGames, fileName, size, numSamples, depth):
	totalMoves = 0
	results = []
	for i in xrange(numGames):
		numMoves = function(fileName, size, numSamples, depth)
		if numMoves == None:
			print("Problem in function {0}".format(function))
			sys.exit(-1)
		else:
			results.append(numMoves)
			totalMoves += currentMoves
	return totalMoves/float(numGames), results


if __name__ == "__main__":
	numGames = 10

	numSamples = 10
	depth = 4
	fileName = "builtin4.txt"
	print("Using file = {0}".format(fileName))
	for depth in [3,4,5]: #,6,7,8]:
		for numSamples in [14, 16, 18]: #8,10,12,14,16]:

			print("Running PNGS with numGames = {2}, depth = {0} and numSamples = {1}".format(depth, numSamples, numGames))
			PNGSAverage, MCAverage, findTime, pngsTime, PNGSResults = playMultiplePNGSGames(runPNGSPlayerFirstSol, numGames, fileName, 16, numSamples, depth)
			#print(PNGSDict)
			print("Average Number of Moves Per Game = {0}".format(PNGSAverage))
			print("Average Number of Moves Per Game Before Improvement = {0}".format(MCAverage))
			print("Average findTime per game = {0}".format(findTime))
			print("Average pngsTime per game = {0}".format(pngsTime))
			print(PNGSResults)
			print("")

	'''
	print("Running Greedy with numGames = {0}".format(numGames))
	PNGSAverage, MCAverage, findTime, pngsTime, PNGSResults = playMultiplePNGSGames(runGreedyPlayerFirstSol, numGames, fileName, 16, numSamples, depth)
	#print(PNGSDict)
	print("Average Number of Moves Per Game = {0}".format(PNGSAverage))
	print("Average Number of Moves Per Game Before Improvement = {0}".format(MCAverage))
	print("Average findTime per game = {0}".format(findTime))
	print("Average pngsTime per game = {0}".format(pngsTime))
	print(PNGSResults)
	print("")
	'''

	
	'''tstart = time.clock()
	print("Running Rand with numGames = {0}".format(numGames))
	RandAverage, RandDict = playMultipleGames(runRandomPlayerFirstSol, numGames, fileName, 16, numSamples, depth)
	#print(RandDict)
	print("Average Number of Moves Per Game = {0}".format(RandAverage))
	print("Average time per game = {0}\n".format((time.clock() - tstart)/ numGames))
	'''




















