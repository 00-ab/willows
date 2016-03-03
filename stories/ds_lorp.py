from tools.choose import choose as choose
import rules.dr_default as rules
import display.dd_console as display
import copy
import sys
import json


character = {
		"punchiness" : 0,
		"barbosity" : 0,
		"slickitude" : 0,
		"pluchritude" : 0,
		"justicality": 0
		}

def setup():
	self = copy.deepcopy( character )
	return self

# DANCE MECHANISM SECTIONS
def setup_dance( self ):
	"""
	dE/A/F/W represents the defendant's earth, air, fire, and water.
	pE/A/F/W represents the prosecutor's earth, air, fire, and water.
	"""
	# The prosecutor is always the same.
	pE = 10
	pA = 10
	pF = 10
	pW = 10

	# The defentant is determined by previous choices.
	dE = 10
	dA = 10
	dF = 10
	dW = 10

	# Punchiness bonus boosts fire and air
	dF += self["punchiness"]
	dA += self["punchiness"]

	# Barbosity bonus boosts fire and water
	dF += self["barbosity"]
	dA += self["barbosity"]

	# Slickitude bonus boosts air and water
	dA += self["slickitude"]
	dW += self["slickitude"]

	# (Will is nearly useless, since losing any will ends the dance.)

	dance = rules.set_stage(
			dE, dA, dF, dW,
			pE, pA, pF, pW,
			2, 0 )
	return dance

def prosecutor_ai():
	pass

def narrate_actions():
	"""
	For DEFENDANT:
	advance = truth
	retreat = backpedal
	breathe = disreply
	evade = play dumb
	tease = annoy the prosecutor

	For PROSECUTOR:
	advance = pursue
	retreat = backpedal
	breathe = think
	"""
def check_distance():
	pass

def check_air():
	pass

def check_water():
	pass

def check_fire():
	"""
	Fire correlates in this case with anger or passion.
	If heat == fire, the defendant should know
	that it is furious and likely to make a mistake
	"""

def check_earth():
	"""
	The defendant has lost when its will is damaged.
	(Even a little.)
	The prosecutor has lost when his will is exhausted.
	"""

# STORY SECTIONS

def ONE( self ):
	print("""
	Lorp Masson, the pious of Dr. Hat,
	sent Waddleston Emissary town to Tybalt Lane
	to oversee the booming of the goliath.

	Now this was overseas,
	and as such it was naturally underdone.
	The banions were paltry,
	but red, white, and blue nonetheless,
	so we threw our hats in the air
	and sung along with the band,
	though it was only three pieces
	and their drums were worn.

	Well, that was Labour Day,
	and naturally we came away from it...
	but, who knows?
	Maybe some good came of it anyway.

	Now you, sir.
	What did you say to Tybalt on that day?

	["Said he was a right thwacker, sir."]
	["Called him a buffoon."]
	["Told him to get out of it."]
	["Beat him right off."]
	""")

	choice = choose( "thwacker", "buffoon", "get out", "beat" )

	print("""
	Of course you did.
	""")
	raw_input()

	if choice == "thwacker":
		self["punchiness"] += 5
		self["barbosity"] += 2
		self["slickitude"] += 1
	elif choice == "buffoon":
		self["punchiness"] += 3
		self["barbosity"] += 4
		self["slickitude"] += 1
	elif choice == "get out":
		self["punchiness"] += 3
		self["barbosity"] += 2
		self["slickitude"] += 3
	else:
		self["punchiness"] += 4
		self["barbosity"] += 4
	
	return self

def TWO( self ):
	print( """
	Now, Tybalt was bearing papers that time,
	papers bourne to him by Waddleston Emissary,
	signed in the name of Dr. Hat
	and sealed with his personal signet,
	asserting his right to trundle the left-wight spigot.

	Did he produce those papers for you?

	["He did not."]
	["He denied having papers."]
	["He had no such papers."]
	["Yes, I saw them."]
	""")
	choice = choose( "not", "denied", "none", "saw" )

	if choice == "not":
		print("""
			He didn't ask for 'em, yr'onor!
		""")
		self["justicality"] += 1
	elif choice == "denied":
		print("""
			That is a heinous lie, yr'honor!
		""")
		self["justicality"] -= 1
		
	elif choice == "none":
		print("""
			That is a heinous lie, yr'honor!
		""")
		self["justicality"] -= 1
	else:
		print("""
			Damn right he did!
		""")
	print("""
	Your testimony has been heard, Mr. Tybalt.
	""")
	raw_input()

	return self
	

def THREE( self ):
	print("""
	Whenceward and upward, you heard
	that fairness was gone out of it:
	the command was granted,
	and you were all to clear out.
	Now, it is well-established:
	that you had been informed
	of the nature of the edict
	and its suchwhile surveillance.

	You're under key with it, sir?

	["I am, sir."]
	["I am not, sir."]
	""")

	choice = choose( "am", "not" )

	if choice == "am":
		pass
	else:
		self["punchiness"] += 2
		self["barbosity"] += 2
		self["slickitude"] -= 2
		print("""
	Don't you play dumb with me,
	you young snappit!
	I've seen your test results
	and they're nothing to play around with.
	Now, if you don't understand,
	I shall explain for you in simpler terms,
	but I shall only warn you once:
	you fuck with this court
	and you shall be held in contempt.

	Now, hear me:
	Witnesses attest to your being informed
	of the nature of Mr. Tybalt's mission.
	Multiple witnesses.
	Is this not the case?

	["Yes."]
	["No."]
	""")
		choice = choose( "yes", "no" )
		if choice == "yes":
			pass
		else:
			print("""
	I hold the witness in contempt of court.
	The remainder of the trial
	will be conducted in its absence.
		""")
			raw_input()
			sys.exit()

	print("""
	Very well then, let's proceed.
	""")
	raw_input()

	return self

def FOUR( self ):
	print("""
	There is one more matter
	of which I want to assure myself.

	Your wife, Mrs. Mason, I'm sure you remember her,
	the hermwig in the white dress,
	she came up here and spoke to us
	a minute before you got in,
	and she told us that you justified yourself
	that day and hereafter, publicly,
	as regards your actions on that day.

	You're certainly aware of the pernicious malevolences,
	their threat to the throne,
	the obwobbles, syndromes, and various Disguises,
	with which are manifest the baseries
	and the various vilenesses
	that do strive to undo us.
	And you are naturally aware
	of the effect such words might have.

	I ask you to justify yourself --
	though bear in mind that no justification
	is a legitimate defense
	for having contradicted an edict composed of Royal Power --
	I ask you to justify yourself
	here, in this courtroom,
	in the same manner in which you have justified yourself publicly
	in past and in presence of masses.

	["It was a matter of justice."]
	["It was a matter of public safety."]
	["I was simply angry."]
	["Go fuck yourself."]
	""")
	choice = choose( "justice", "safety", "angry", "fuck" )
	if choice == "justice":
		print("""
		The Royal Power is the only justice
		with which this court is concerned, sir.
		I don't know what kind of tribal law you follow,
		but your alternate system of ethics
		does not enter into the matter.
		""")
		self["pluchritude"] += 2
		self["barbosity"] += 2
		self["punchiness"] += 2
		self["slickitude"] -= 2
	elif choice == "safety":
		print("""
		Well, is that so?
		Naturally, you would be an expert in the matter.
		Well.

		Should it turn out to be the case
		that there is justification for your actions
		on the grounds of public safety
		then you may expect a Royal Pardon.
		But that is not the business of this court,
		so I suggest you keep your defense in order.
		""")
		self["slickitude"] += 4
		self["punchiness"] += 2
	elif choice == "angry":
		print("""
		Well, at least you are honest.
		""")
		self["punchiness"] += 4
		self["barbosity"] += 4
		self["slickitude"] -= 2
	else:
		print("""
	Why thank you!
		""")
		raw_input()
		print("""
	That makes the matter much easier!
	I was hoping I might have the day off today,
	and you, child, have just made it possible.

	(BANG OF GAVEL)

	I find the defendent in contempt of court
	and sentence it to death.

	Court adjourned till the morrow.
		""")
		sys.exit()

	return self

def start():
	self = setup()
	self = ONE( self )
	self = TWO( self )
	self = THREE( self )
	self = FOUR( self )

	dance = setup_dance( self )
	dance_json = json.dumps( dance )
	display.display( dance_json )

	"""
	dance_over = 0
	while dance_over == 0:
		pass
		"""
