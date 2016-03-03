from __future__ import print_function
import math
import copy
import json

dancer = {
		verbs : {}
		adjs: {}
		}

# dancer describes the state of a conscious being
# relation describes the feeling of one regarding another

dancer["adjs"]["lust"]
dancer["adjs"]["like"]

# define the archetypal relations

dancer["relation"]["arch"] = {
		"lust" : 0,
		"like" : 0,
		"respect" : 0,
		}

# define the dancer's abilities

## API:

# MODULE SETTINGS:
# These values used to calibrate action effects.
SMALL_MULTIPLIER = 0.1
MEDIUM_MULTIPLIER = 0.2
LARGE_MULTIPLIER = 0.4

# Key bindings. These are inserted into the game object during _setup_player.
keyDict = {
		"y" : "touch",
		"t" : "evade",
		"r" : "jest",
		"f" : "retreat",
		"g" : "breathe",
		"h" : "advance"
		}

# Lists -- these are to be used by the client.
# (Mainly so display functions can be dynamic.)
# My dance_display.py should work for any moveList that is a list of strings
# and any statList that is a list of strings
# or a list of lists which contain only strings.
# BUT: moveList + statList MUST == the keys of p in _setup_player (-'choice')
# (I know that's ugly, sorry.)
moveList = [ 'advance', 'retreat', 'touch', 'evade', 'breathe', 'jest' ]
statList = [ ['earth', 'will'], ['air', 'calm'], ['fire', 'heat'], ['water', 'balance'] ]
playerList = ['0', '1']

# These are some special exceptions.
# Probably not necessary.
class NoSuchMove( Exception ):
	pass

class NoSuchStat( Exception ):
	pass

class IllegalMove( Exception ):
	pass

class GameOver( Exception ):
	pass

## BACKEND:

# UTILITY FUNCTIONS
# These are totally useless ;)

# SMALL

def _small( mag ):
	value = ( mag * SMALL_MULTIPLIER )
	return (value)

# MED
def _med( mag ):
	value = ( mag * MEDIUM_MULTIPLIER )
	return (value)

# LARGE
def _large( mag ):
	value = ( mag * LARGE_MULTIPLIER )
	return (value)


def _setup_player( e0, a0, f0, w0):
	"""
	Accepts initial values for eafw,
	returns a complete player object.
	"""
	heat = f0/2
	if f0%2 == 1: heat += 1

	p = {
		'earth' : float(e0),
		'will' : float(e0),
		'air' : float(a0),
		'calm' : float(a0),
		'fire' : float(f0),
		'heat' :float(heat),
		'water' : float(w0),
		'balance' : -1.0,

		'choice' : None,

		'advance' : 1,
		'retreat' : 1,
		'touch' : 1,
		'evade' : 1,
		'breathe' : 1,
		'jest' : 1
		}
	p.update( keyDict )
	return p

def _execute( player, choice, game_data0, game_data1 ):
	"""
	Reads from gd0 and writes to gd1,
	according to the move with the same name as the player's choice.
	"""
	# In theory, neither of the below exceptions should ever be raised
	# since the client-side function should test both conditions
	# before calling a new turn.

	# First check to see if the move exists.
	if choice in moveList:
		pass
	else:
		raise NoSuchMove
	# Second check to see if the move is currently allowed.
	if game_data0[ str(player) ][ str(choice) ] == 1:
		pass
	else:
		raise IllegalMove

	# Then perform the move.
	if player == 0:
		other = 1
	else:
		other = 0
	move = execList[ choice ]
	game_data1 = move( str(player), str(other), game_data0, game_data1)

	# Finally, return the modified object.
	return game_data1

def _enables( game_data ):
	for move in moveList:
		game_data['0'][move] = 1
		game_data['1'][move] = 1
	return game_data

def _disables( game_data ):
	# First learn which moves were just used...
	choice0 = game_data['0']['choice']
	choice1 = game_data['1']['choice']

	# ... then disable both of them for the next round.
	game_data['0'][choice0] = 0
	game_data['1'][choice1] = 0
	return game_data

def _val_in( val_0, magnitude ):
	"""
	Returns magnitude with the sign such that abs(val_0 + mag2) < abs(val_0) 
	If mag < 0, does the opposite.
	If abs(mag) > 1, may result in an overshoot.
	"""
	if val_0 < 0:
		pass
	elif val_0 > 0:
		magnitude = -magnitude
	else:
		# Because one cannot draw closer to 0 if one is already there:
		if magnitude > 0: magnitude = 0
		# And since we don't want d to be always negative:
		else: magnitude = -magnitude

	return magnitude

def _gameover_check( game_data ):
	"""
	Checks to see if gameover should be declared.
	This function defines the encounter-end conditions.
	(Maybe it should take some cues from ## MODULE SETTINGS ?)
	"""
	if game_data["0"]["will"] <= 0 and game_data["1"]["will"] <= 0:
		game_data['game']['gameover'] = 1
		game_data['game']['gameover_message'] = ( 'SimultaneousExhaustion' )
	else: 
		for p in range( 0, 1 ):
			if game_data[ str(p) ]['will'] <= 0:
				game_data['game']['gameover'] = 1
				game_data['game']['gameover_message'] = ( 'Player ' + str(p) + ' exhaustion.' )

# VERBS SECTION
# This section should include callable functions for each move.
# Each move must accept actor, target, and distance arguments.
# All functions in this section accept a bin for actor or target.
# They read only from game_0 and write only to game_1,
# returning game_1

def _advance( actor, target, game_0, game_1):
	"""
	Signifies a closening, with or without physical contact.
	A bold statement, a step forward, or a glorious charge.
	Costs calm; reduces balance.
	"""
	# This part is the cost. It will always be the same.
	game_1[actor]['calm'] -= _small( game_0[actor]["heat"] )

	# Advancing does not increase one's balance
	# if one pushes against the target.
	# (Though frict may change balance.)
	if not ( game_0['game']['d'] == 0 and _get_future_d( game_0 ) ):
		game_1[actor]['balance'] += 1
	
	# If the future distance is 0, a collision occurs.
	# (As long as the target did not evade.)
	if _get_future_d( game_0 ) == 0 and game_0[target]['choice'] != 'evade':
		game_1 = _frict( actor, target, game_0, game_1 )

	# If the two players are already grappling,
	# (ie in the same space, at d=0)
	# they cannot advance past each other.
	# Otherwise, the distance will decrease.
	# (If they are at d1, they will switch positions.)
	game_1['game']['d'] += _val_in( game_0['game']['d'], 1 )
	
	return game_1

def _retreat( actor, target, game_0, game_1):
	"""
	Signifies a distancing, a retreat, a coldness
	a disreply, a shyness, a step back, or a flight.
	Costs calm; reduces balance.
	"""
	# Reduce calm by small
	game_1[actor]['calm'] -= _small( game_0[actor]["heat"] )

	# Decrease balance by small
	game_1[actor]['balance'] -= 1

	# Open distance by 1
	if game_0[target]['choice'] == 'advance' and game_0['game']['d'] == 0:
		pass
	else:
		game_1['game']['d'] += _val_in( game_0['game']['d'], -1 )

	return game_1

def _touch( actor, target, game_0, game_1):
	"""
	Signifies phsyical contact.
	A brush, caress, strike, grope, or attempt.
	"""
	# This is the cost
	game_1[actor]['calm'] -= _med( game_0[actor]['heat'] )

	# Check to see if the move connects.
	if abs( _get_future_d( game_0 ) ) <= 1 and game_0[target]['choice'] != 'evade':
		# Below is a somewhat silly way of saying
		# that a successful touch is like a frict,
		# but only affecting the target.
		save = copy.deepcopy( game_1[actor] )
		_frict( actor, target, game_0, game_1 )
		game_1[actor] = copy.deepcopy( save )

	return game_1

def _evade( actor, target, game_0, game_1):
	"""
	A sort of dodge or refusal.
	Counteracts the effect of a touch or advance. Rather embarassing against a tease.
	Technically does nothing. Other acts may define exceptions for: if game_0[target]['choice'] == 'evade':
	"""
	if _frict_occurs( game_0 ):
		# In this case, _frict_occurs() is _if_frict_would_occur()
		# If successful, restores calm.
		# (Since you look so cool.)
		game_1[actor]['calm'] += _small( game_0[actor]['air'] )
	else:
		# Otherwise, costs a fair bit.
		game_1[actor]['calm'] -= _med( game_0[actor]['heat'] )

	return game_1

def _breathe( actor, target, game_0, game_1):
	"""
	A moment of rest, contemplation, and gathering.
	Could signify literal breathing, but also meditation or inaction.
	(Totally restores calm. Slightly reduces heat and restores will.)
	"""
	# See above.
	if not _frict_occurs( game_0 ):
		game_1[actor]['calm'] = game_0[actor]['air']
		game_1[actor]['heat'] -= _small( game_0[actor]['air'] )
		game_1[actor]['will'] += _small( game_0[actor]['air'] )
		# Closes balance by one.
		game_1[actor]['balance'] += _val_in( game_1[actor]['balance'], 1 )
	# However: breathe is interrupted by a frict.
	# You'll still get some breath back, but receive no other bonuses.
	else:
		game_1[actor]['calm'] += _large( game_0[actor]['air'] )

					
	return game_1

def _jest( actor, target, game_0, game_1):
	"""
	A joke or strangeness, encouraging advance and curiosity
	by inspiring a passion -- for example anger or desire.
	(Adds heat and negative balance -- more effective if the target is retreating or evading.)
	"""
	game_1[actor]['calm'] -= _small( game_0[actor]['heat'] )
	if not game_0[target]['choice'] == 'breathe':
		game_1[target]['heat'] += _small( game_0[actor]['heat'] )
		# By reducing balance, tease can force the target to advance or suffer in fricts
		# It is less useful if the player is already forward-balanced.
		game_1[target]['balance'] -= 1

	if game_0[target]['choice'] == 'retreat' or game_0[target]['choice'] == 'evade':
		game_1[target]['heat'] += _med( game_0[actor]['heat'] )

	return game_1

def _frict_occurs( game_0 ):
	for p in playerList:
		if game_0[str(p)]['choice'] == "advance" and _get_future_d( game_0 ) == 0:
			return 1
		elif game_0[str(p)]['choice'] == "touch" and abs(_get_future_d( game_0 )) <= 1:
			return 1
		else:
			pass
	return 0


def _frict( actor, target, game_0, game_1):
	"""
	Represents a kind of clash, collision, or rubbing-together.
	Depends on balances.
	"""
	# Both players receive heat. The one with less receives more.
	game_1[target]['heat'] += _small( game_0[actor]['fire'])
	game_1[actor]['heat'] += _small( game_0[target]['fire'])

	if game_0[actor]['heat'] > game_0[target]['heat']:
		game_1[target]['heat'] += _small( game_0[actor]['heat'] )
	elif game_0[actor]['heat'] < game_0[target]['heat']:
		game_1[actor]['heat'] += _small( game_0[target]['heat'] )
	else:
		game_1[target]['heat'] += _small( game_0[actor]['heat'] )
		game_1[actor]['heat'] += _small( game_0[target]['heat'] )

	
	# If one player's will is less than 25% of the other's
	# that player will be pushed back.
	if game_0[actor]['will'] > 4 * game_0[target]['will']:
		game_1[target]['balance'] -= 1
	elif 4 * game_0[actor]['will'] < game_0[target]['will']:
		game_1[actor]['balance'] -= 1

	# Adds heat to each player, giving the advantage to the player
	# whose absolute balance is the smaller percent of their water.
	# (So if p0.bal = 1/10 and p1.bal = -1/11, then p1 will have the advantage.)
	a_bal = float( abs(game_0[actor]['balance'] )) / game_0[actor]['water']
	t_bal = float( abs(game_0[target]['balance'] )) / game_0[target]['water']
	if a_bal == t_bal:
		game_1[actor]['heat'] += _med( game_0[target]['heat'] )
		game_1[target]['heat'] += _med( game_0[actor]['heat'] )
	elif a_bal > t_bal:
		game_1[actor]['heat'] += _large( game_0[target]['heat'] )
		game_1[target]['heat'] += _small( game_0[actor]['heat'] )
	elif a_bal < t_bal:
		game_1[actor]['heat'] += _small( game_0[target]['heat'] )
		game_1[target]['heat'] += _large( game_0[actor]['heat'] )
	else:
		print( "I think this is impossible, right?" )
	
	return game_1

def _get_future_d( game_0 ):
	"""
	This somewhat kludgy function calculates the future distance
	based on the present distance and the player choices.
	Used in collision detection.
	"""
	d = game_0['game']['d']
	if d == 0 and ( game_0['0']['choice'] == 'advance' or game_0['1']['choice'] == 'advance' ):
		pass
	else:
		for p in range( 2 ):
			choice = game_0[str(p)]['choice']
			if choice == 'advance':
				d -= math.copysign(1, d)
			elif choice == 'retreat':
				d += math.copysign(1, d)
			else:
				pass
	d = int(d)
	return d


# The below is used by _execute() to link strings with actions.
# This is a little silly, but I don't know a better way.
# (For some reason, this list can't be written until after the functions it contains.
# Fuck you, Python.)
execList = {
		"advance" : _advance,
		"retreat" : _retreat,
		"touch" : _touch,
		"evade" : _evade,
		"breathe" : _breathe,
		"jest" : _jest
		}

# ADJECTIVES SECTION
# This section should include rules for checking and correcting element statuses.
	
def _adj_check( game_data ):
	# Checks all play adjective/attributes/stats in sequence.
	game_data = _air_check(   game_data) # ; - )
	game_data = _fire_check(  game_data)
	game_data = _water_check( game_data)
	game_data = _earth_check( game_data) 
	return game_data

def _earth_check( game_data ):
	"""
	Without will,
	an individual is unable to continue.
	"""
	for p in range(2):
		if game_data[str(p)]['will'] > game_data[str(p)]['earth']:
			game_data[str(p)]['will'] = game_data[str(p)]['earth']

	if game_data['0']['will'] <= 0 and game_data['1']['will'] <= 0:
		game_data['game']['gameover'] = 1
		game_data['game']['gameover_message'] = 2
	else:
		for p in range( 2 ):
			if game_data[str(p)]['will'] <= 0:
				game_data['game']['gameover'] = 1
				game_data['game']['gameover_message'] = p

	return game_data


def _air_check( game_data ):
	"""
	Below-min breath is called exhaustion.
	Knowing when to breathe is important.
	"""
	for p in range( 2 ):
		c = game_data[str(p)]['calm']
		# Punish will if calm is below zero
		if c < 0:
			game_data[str(p)]['calm'] = 0
			game_data[str(p)]['will'] += c
		# Treat Air as maximum Calm
		if c > game_data[str(p)]['air']:
			game_data[str(p)]['calm'] = game_data[str(p)]['air']

	return game_data

def _fire_check( game_data ):
	"""
	Above-max heat is called mania,
	while below-min heat is called depression.
	High heat will power-up some moves, but it is risky.
	"""
	for p in range(2):
		h = game_data[str(p)]['heat']
		f = game_data[str(p)]['fire']
		if h < 0:
			game_data[str(p)]['heat'] = 0
			game_data[str(p)]['will'] += h
		if h > f:
			game_data[str(p)]['heat'] = f
			game_data[str(p)]['will'] -= ( h - f )
	return game_data

def _water_check( game_data ):
	"""
	Balance is not a magnitude, but a distance from zero.
	Zero represents perfect balance,
	while the positive represents forwardness and the negative backwardness.
	"""
	for p in range( 2 ):
		b = game_data[str(p)]['balance']
		w = game_data[str(p)]['water']
		if abs( b ) > w:
			game_data[str(p)]['will'] -= ( abs( b ) - w )
			if b < 0:
				game_data[str(p)]['balance'] = -w
			elif b > 0:
				game_data[str(p)]['balance'] = w
	return game_data

# THESE ARE MINOR AND NONMANDATORY API FUNCTIONS,
# BUT THEIR USE IS RECOMMENDED

def get_stat( dance, player, stat ):
	"""
	Accepts a bin representing the player
	and a string representing the stat
	and returns the stat's value.
	"""
	return dance[ str(player) ][ str(stat) ]

def mod_stat( dance, player, stat, magnitude ):
	dance[ str(player) ][ str(stat) ] += int( magnitude )
	return dance

def set_stat( dance, player, stat, magnitude ):
	dance[ str(player) ][ str(stat) ] = int( magnitude )
	return dance

def get_dist( dance ):
	return dance[ "game" ][ "d" ]

def mod_dist( dance, magnitude ):
	dance[ "game" ][ "d" ] += int( magnitude )
	return dance

def set_dist( dance, magnitude ):
	dance[ "game" ][ "d" ] = int( magnitude )
	return dance
	
# THE TWO FUNCTIONS BELOW
# ARE THE ONLY ESSENTIAL API FUNCTIONS
def set_stage( p0_e, p0_a, p0_f, p0_w, p1_e, p1_a, p1_f, p1_w, d0, d_max ):
	"""
	Accepts initial element values for p0 and p1,
	as well as initial and maximum distance,
	then returns a JSON object describing the game-stage.
	"""
	game_data = { 
		'0' : _setup_player( p0_e, p0_a, p0_f, p0_w ),
		'1' : _setup_player( p1_e, p1_a, p1_f, p1_w ),
		'game' : {
			'd' : d0,
			'd_max' : d_max,
			'turn' : 0,
			'0choice' : None,
			'1choice' : None,
			'gameover' : 0,
			'gameover_message' : "ERROR" 
			# in 'gameover_message', a bool will symbolize that player, a 2 will symbolize both players 
			}
		}
	json_data = json.dumps( game_data )
	return json_data

def turn( json_data ):
	"""
	Accepts a JSON object describing the game-stage,
	plus a binary representing the active player
	and a string representing that player's choice.
	Returns a modified JSON object.
	"""
	# Open the game data
	game_data0 = json.loads( json_data )
	
	# These exceptions should make it easy
	# to learn if player behavior has violated the rules.
	if game_data0['game']['gameover'] == 1:
		raise GameOver
	for player in playerList:
		choice = game_data0[player]['choice']
		if not choice in moveList:
			raise NoSuchMove
		if game_data0[player][choice] == 0:
			raise IllegalMove

	# Split the game_data into two branches: 0 for reading and 1 for writing.
	# For this reason, all action functions must use +/-=, not just =
	game_data1 = copy.deepcopy( game_data0 )

	# Execute the moves of each player
	game_data1 = _execute( 0, game_data0['0']['choice'], game_data0, game_data1 )
	game_data1 = _execute( 1, game_data0['1']['choice'], game_data0, game_data1 )

	# Reenable all moves.
	game_data1 = _enables( game_data1 )

	# Disable for next round the moves that were just used.
	game_data1 = _disables( game_data1 )

	# Check to see if any stat is outside legal bounds
	game_data1 = _adj_check( game_data1 )

	# Check to see if the game has ended
	_gameover_check( game_data1 )

	# Finally, increment the turn counter.
	game_data1['game']['turn'] += 1

	# Write the log

	# Repackage and return the game data
	new_json_data = json.dumps( game_data1 )
	return new_json_data

