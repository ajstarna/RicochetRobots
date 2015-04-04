#!/usr/bin/python


''' this file contains unit tests for the graph. '''

import GraphModule
import sys, traceback


def testInit(name):
	
	state = (0,1,2,3,9,8,10,3)
	dict = {}
	dict[state] = "test"
	try:
		graph = GraphModule.Graph()
		if graph.graphDict != {}:
			return 0
		
		graph2 = GraphModule.Graph(dict)
		if graph2.graphDict != dict:
			return 0

		return 1

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0



def testAddNode(name):
	state = (0,1,2,3,9,8,10,3)
	try:
		graph = GraphModule.Graph()
		graph.addNode(state)
		
		if not state in graph.graphDict:
			return 0
		return 1

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0


def testEdge(name):
	state = (0,1,2,3,9,8,10,3)
	try:
		graph = GraphModule.Graph()
		target = (0,0,1,1,2,2,3,3)
		moveNum = 3
		graph.addNode(state)
		graph.addEdge(state, target, moveNum)
		
		if not state in graph.graphDict:
			print("not in graph dict")
			return 0
		
		if graph.graphDict[state][0].targetState != target:
			print("not a target match")
			return 0
		if graph.graphDict[state][0].moveNum != moveNum:
			return 0
		
		return 1

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0
	return


def testConvertRobotDict(name):
	dict = {}
	dict[0] = (0,0)
	dict[1] = (1,1)
	dict[2] = (2,2)
	dict[3] = (3,3)
	
	try:
		g = GraphModule.Graph()
		tuple = g.convertRobotDictToTuple(dict)
		if tuple != (0,0,1,1,2,2,3,3):
			return 0
		
		return 1

	except:
		print("exception in {}".format(name))
		traceback.print_exc(file=sys.stdout)
		return 0
	return


if __name__ == "__main__":

	tests = [testInit, testAddNode, testEdge, testConvertRobotDict]


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




