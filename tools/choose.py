import sys # for sys. exit
def choose( *args ):
	"""
	Accepts a list of options,
	then traps the player
	until it types one of them.
	"""

	# First prepare to print the list of options.
	string = "["
#	args.append( "quit" )
	for choice in enumerate(args):
		string += choice[1]
		if choice[0] != len(args) - 1:
			string += "/"
	string += "] "

	# Then get the choice.
	valid = 0
	while valid == 0:
		player_choice = raw_input( string )
		if player_choice in args:
			valid = 1
		else:
			print( "Invalid response." )
	
	if player_choice == "quit":
		sys.exit()

	return player_choice
