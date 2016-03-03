from __future__ import print_function # something in dd_console requires this, so I use it throughout
import json # packing and unpacking tasks throughout
import dr_default # This module contains the rules
import dd_console # This module prints the game in a python console
import dai_default

# MODULE SETTINGS

# First set the modules used.
# This makes it easy to switch modules quickly.

rules = dr_default
display = dd_console

# Import some lists from dr
moves = rules.moveList
stats = rules.statList
players = rules.playerList

def one_turn( dance ):
	"""
	One Turn prints the current state of the game,
	gets a move choice from each player,
	then executes them and returns the new state.
	"""

	# Unpack the game data
	game_data = json.loads( dance )

	# Check to see if the game has ended.
	# Break if so.
	if game_data['game']['gameover'] == 1:
		print( game_data['game']['gameover_message'] )
		return 0
		
	# Read that data to print the stats and map
	display.display( dance )

	# Get each player's choice
	# (This is the only part that changes the data.)
	dance = json.dumps( game_data )
	game_data['0']['choice'] = display.get_in(dance, 0)
	ai_psych = dai_default.psych( "aggressive" )
	game_data['1']['choice'] = dai_default.choose( dance, 1, ai_psych )
	print(" ")
	
	# Repack the game data and send it for processing
	# according to the rules.
	dance = json.dumps( game_data )
	
	dance = rules.turn( dance )

	# Return the new data package.
	return dance


# MAIN #

def start():

	dance = rules.set_stage( 10, 10, 10, 10, 10, 10, 10, 10, 2, 0 )
	display.setup_lists( moves, stats, players )
	print( display.moves, display.stats, display.players )

	strng = "\n\n   _-~-:: Welcome to Dance ::-~-_\n\n"
	print( strng )

	dance_over = 0
	while dance_over == 0:
		dance = one_turn( dance )
		if dance == 0:
			dance_over = 1

	strng = "\n\n   ~-_-:: The End ::-_-~\n\n"
	print( strng )
