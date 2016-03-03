def read( script, flag ):
"""
For a script dilineated into sections headed by flags starting with "## ",
finds the section with the passed-in flag and returns it.
Ignores lines starting with single #s. See /script/example .
"""
	for line in script:
		if line[0:2] == "## " and line[3:] == flag:
			text = []
			toRead = line + 1
			while not script[toRead][0:2] == "## ":
				#ignore comments
				if script[ toRead ][0] == "#":
					toRead += 1
				#strip out blank lines at end of passages
				#(I like having those lines in cause it makes scripts pretty.)
				elif script[ toRead ] == "" and script[ toRead + 1 ][0:2] == "## "
					toRead += 1
				#add true lines to output
				else:
					text.append( script[ toRead ] )
					toRead += 1
			return text

def genFlagList( dance ):
"""
Accepts a dance object and returns a list of flags.
This is akin to reading or parsing the condition of the dance game.
The flags can then be read using read().
"""
	flagList = []
	
	#parse distance
	distance = dance["game"]["d"]
	if distance = 0:
		flagList.append( "grapple" )
	elif abs(distance) = 1:
		flagList.append( "shortRange" )
	elif abs(distance) = 2:
		flagList.append( "midRange" )
	elif abs(distance) = 3:
		flagList.append( "longRange")
	elif abs(distance) >= 4:
		flaglist.append( "far" )

def narrate( dance, script ):
"""
This accepts a dance, gets all relevant flags, and returns their corresponding scripts.
In your games, you may wish to narrate flags in a certain order,
so this may be too blunt for you.
"""
# in fact this might be too blunt for everyone...
# how do I make it more versatile?

	narrative = []

	flagList = genFlagList( dance )
	for flag in flagList:
		narrative += read( script, flag )
	return narrative
