from __future__ import print_function
import dance_game
import json
import getch # for get_in
import sys # for sys.exit in get_in

moves = dance_game.moveList
stats = dance_game.statList
players = [ 0, 1 ]

# Symbols for the map
divSym = ":"
horizonSym = divSym*90
p0Sym = " X "
p1Sym = " O "
bothSym = " & "
terrainSym = " _ "
hardWallSym = "###" # Used when (d-d_max)%2 = 0
leftSoftWallSym = "##_ " # Used when (d-d_max)%2 = 1
rightSoftWallSym = " _##" # Used when (d-d_max)%2 = 1
borderCh = "#"
voidSym = "   "

def display( dance ):
	game_data = json.loads( dance )
	"""
	Displays the current state of the game.
	"""
	_draw_header( game_data )
	_draw_last_moves( game_data )
	print("\n" + horizonSym + "\n")
	_draw_stats( game_data )
	print("\n" + horizonSym + "\n")
	_draw_map( game_data )
	print("\n" + horizonSym + "\n")
	_draw_moves( game_data )
	print("\n" + horizonSym + "\n")
	_draw_keys( game_data )
	print("\n" + horizonSym + "\n")

def _draw_header( game_data ):
	strng = "\n\n   _-:: Turn " + str(game_data['game']['turn']) + " ::-_\n\n"
	print( strng )

def _draw_last_moves( game_data ):
	if game_data['0']['choice'] != None:
		print( "Last turn:" )
		print( "Player 0 used: " + game_data['0']['choice'] )
		print( "Player 1 used: " + game_data['1']['choice'] + "\n" )


def get_in( dance, player ):
	"""
	Accepts a compressed dance game object and a player binary.
	Returns that player's choice.
	"""
	game_data = json.loads( dance )

	valid = 0
	strng = "Player " + str(player) + " input choice: "
	while valid == 0:
		print( "\n" + strng ),
		key = getch.getch()
		if key == chr(27):
			# Esc = hard quit
			sys.exit()
		elif key == "q":
			# q = soft quit
			game_data['game']['gameover'] = 1
			game_data['game']['gameover_message'] = "Player " + str(player) + " quit."
			valid = 1
		elif key in game_data[str(player)]:
			choice = game_data[str(player)][key]
			if game_data[str(player)][choice] == 1:
				valid = 1
				print( "Accepted." )
			else:
				print( "That move is presently illegal. Please choose another." )
		else:
			print( "That move does not exist. Please choose another." )
	return choice

def _draw_stats( game_data ):
	for item in stats:
		# This segment called if statList is flat
		if type(item) == str:
			outstr = ""
			for p in players:
				strng = "Player {0} {1:10} : {2:d5}".format( p, item, game_data[p][item] )
				outstr += strng
			print( outstr )
		# This segment called if statList is a list of lists
		# It will fail if statList has three or more dimensions.
		elif type(item) == list:
			outstr = divSym*3 + " " #hardcoding strings that will never change
			for p in players:
				#string0 will name the stats
				#string1 will give their values
				#string 1 belongs on the end of string 0
				strng0 = "Player {0} [{1}".format( p, divSym )
				strng1 = "{0}".format(divSym)
				for stat in item:
					if type(stat) == str:
						strng0 += str( stat ).upper() + divSym
						strng1 += str( game_data[str(p)][stat] ) + divSym
				outstr += "{0:40}".format( " [" + strng0 + strng1 + "]" ) + (divSym*3)
			print( outstr )

def _draw_map( game_data ):
	"""
	Prints the present and max distance,
	then prints an ASCII map representation
	of the players' relative positions.
	"""
	# Store the present and max d as local variables
	d = game_data['game']['d']
	d_max = game_data['game']['d_max']

	# Print the present and max distance
	if d_max == 0:
		print( "Distance = {0}".format( d ))
	else:
		print( "Distance = {0}/{1}".format( d, d_max ))

	# Print the map:
	# Add the left side/wall
	if d_max == 0:
		strng = voidSym + terrainSym
	else:
		d_diff = d_max - abs(d)
		if d_diff % 2 == 0:
			strng = voidSym + hardWallSym*2 + terrainSym*(d_diff/2)
		else:
			strng = voidSym + hardWallSym + leftSoftWallSym + terrainSym*((d_diff-1)/2)

	# Add the players and the space between
	if d == 0:
		strng += bothSym
	else:
		between = ""
		for n in range( abs(d) - 1 ):
			between += terrainSym
		if d < 0:
			strng += p0Sym + between + p1Sym	
		elif d > 0:
			strng += p1Sym + between + p0Sym
	# Add the right side/wall
	if d_max == 0:
		strng += terrainSym + voidSym
	else:
		d_diff = d_max - abs(d)
		if d_diff % 2 == 0:
			strng += terrainSym*(d_diff/2) + hardWallSym*2
		else:
			strng += terrainSym*((d_diff-1)/2) + rightSoftWallSym + hardWallSym
	
	# Actually print the stuff
	for n in range( len(strng) ):
		print( borderCh, end="" ),
	print(" ")
	print( strng )
	for n in range( len(strng) ):
		print( borderCh, end="" ), # FIND OUT HOW TO REMOVE THESE SPACES
	print(" ")

def _draw_moves( game_data ):
	for p in players:
		strng = "Player " + str(p) + " acts available: "
		for move in moves:
			if game_data[str(p)][move] == 1:
				strng += move + "; "
		print( strng )

def _draw_keys( game_data ):
	"""
	Prints the key-map.
	Unfortunately only works if both players
	are using the same map.
	"""
	block = voidSym
	def _appender( row, string ):
		for ch in row:
			if ch in game_data["0"]:
				move = game_data["0"][ch]
				moveFancy = move[0].upper() + move[1:]
				string += ch.upper() + " : {0:10} ".format( moveFancy ) + block
		return string
	row0 = "qwertyuiop[]"
	row1 = "asdfghjkl;'"
	row2 = "zxcvbnm,./"
	string0 = _appender( row0, block )
	string1 = _appender( row1, block )
	string2 = _appender( row2, block )
	print( "CONTROLS:\n" + block + "{0:10}".format( "Esc/Q: Quit") + block)
	if string0 != block: print( string0 )
	if string1 != block: print( string1 )
	if string2 != block: print( string2 )
