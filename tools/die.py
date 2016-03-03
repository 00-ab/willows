import random
import math

def d( sides ):
	result = math.floor( random.random() * sides )
	return result

def die_test( sides, tries ):
	array = range( 0, sides) 
	total = 0

	for iterations in range( 0, tries ):
		roll = int( d( sides ) )
		array( roll ) += 1
		total += roll

	print( total )
	print( array )
	"""
	LlL
	"""
