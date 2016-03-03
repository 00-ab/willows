"""
THE WAR OF THE WILLOWS
EPISODE ONE:
	Encounter on the Terrace
"""

from __future__ import print_function # something in dd_console requires this, so I use it throughout
import copy
# import die -- work without it for now
import tools.choose as choose
import json # packing and unpacking tasks throughout
import rules.dr_default as rules # This module contains the rules
import display.dd_console as display # This module prints the game in a python console

# MODULE SETTINGS

title = "The War of the Willows"

moves = rules.moveList
stats = rules.statList
players = rules.playerList
display.setup_lists( moves, stats, players ) 
# This is a stupid way to do what's being done here.

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
	game_data['1']['choice'] = display.get_in(dance, 1)
	print(" ")
	
	# Repack the game data and send it for processing
	# according to the rules.
	dance = json.dumps( game_data )
	
	dance = rules.turn( dance )

	# Return the new data package.
	return dance


# MAIN SCRIPT #

def intro():
	character = {
		"anger" : 0.0,
		"sorrow" : 0.0,
		"determination" : 0.0,
		"peace" : 0.0,
		}
	grove = copy.deepcopy( character )
	citadel = copy.deepcopy( character )
	self = copy.deepcopy( character )

	print( """
They say my family will die by willows:
	we burned their ashes on great pyres,
	worshiped them at our funerals and weddings.
	They were made from our bodies.
	But we grew unthoughtful and wicked.
	We fell away from their worship,
	and oh shit -- did nothing.
	We forgot all about
	the graves of our ancestors.
	(Don't we all die?)

	We'll probably die.
	We were supposed to 
	burn our dead on beech pyres,
	mix this ash with bonemeal
	and the dung of human revellers
	and put willow-root to it.
	We broke this ancient covenant.

	Now the grove is upon us.
""")
	self["anger"] += 2
	
	citadel["determination"] += 10
	citadel["peace"] += 2
	citadel["sorrow"] += 5
	citadel["anger"] += 3
	
	# The grove is beefier than the citadel.
	grove["anger"] += 30
	grove["sorrow"] += 10
	grove["determination"] += 25
	grove["peace"] += 15

	# Now pack everything up for transmission
	# into the next section.
	chars = {
			"grove" : grove,
			"citadel" : citadel,
			"self" : self,
			}
	return chars

# CHAPTER ONE
## Attack of the Willows

def partOne( chars ):
	self = chars["self"]
	citadel = chars["citadel"]
	grove = chars["grove"]


	print("""
CHAPTER ONE
	""")

	# CHOICE ONE:

	raw_input()
	print( """
		And you.

		What do you want?
	""" )

	answer = choose.choose( "power", "love", "peace", "forgiveness" )

	if answer == "power":
		self["anger"] += 12.5 # power, greed, and hate are interrelated
		self["sorrow"] += 1 # ambition rarely begets regret
		self["peace"] += 7.5 # serenity is the path to power
		self["determination"] += 9 # perhaps selfishness is not as strong as empathy
		print("""
	You feel that you're not as strong
	as you once were.

	But then again,
	maybe you're stronger than ever.

		""")
	elif answer == "love":
		self["anger"] += 4 # because love is often lost
		self["sorrow"] += 5 # because love leads to empathy
		self["peace"] += 10 # because the path of love is joyous
		self["determination"] += 10
		print("""
	Isn't love the answer to everything?
		""")
	elif answer == "peace":
		self["anger"] += 1 # because you are not perfect
		self["peace"] += 15 # because you often find what you seek
		self["sorrow"] += 2 # because coolness does not beget sorrow much
		self["determination"] += 10
		# Accidentally destroyed art of cat that was supposed to go here.
		print("""
		You ain't mad.
		""")
	elif answer == "forgiveness":
		# this might be the weakest loadout, but high sorrow is good in the end
		self["anger"] += 3 # your people have failed you, and vice versa
		self["sorrow"] += 10 # you are filled with regret
		self["determination"] += 5 # you are weak-willed and trembling
		self["peace"] = 5 # you are all decomposed
		print("""
	They ripped a child in half.

	Two men threw fire upon one,
	and it stood before their homes
	while it burned to a single pillar
	of black ash.

	They came upon the library
	and they ripped each book to shreds,
	slept than night in the confetti.
		""")
	else: raise Exception

	# AND THE REACTION TO YOUR CHOICE
	if citadel["anger"] < self["anger"]:
		citadel["peace"] -= 1 # because of your influence
		print("""
		Love is a word for the weak:
		let them hear it stamped out!

		We will not be annihilated because of love!
		""")
	elif self["anger"] < citadel["anger"]:
		self["sorrow"] += 1
		print("""
		"Love is a word for the weak:
		let them hear it stamped out!"

		"We will not be annihilated because of love!"
		""")
	else:
		print("""
		The world seems strange to you.

		Are you asleep?
		""")

	if self["peace"] > grove["peace"]:
		self["peace"] += 2
		grove["peace"] += 2
		citadel["peace"] += 2
		print("""
		Have no fear for this.

		It is a matter of mistakes.

		Let us be grateful.
		""")
	elif self["peace"] == grove["peace"]:
		self["peace"] += 1
		grove["peace"] += 1
		citadel["peace"] += 1
		print("""
		A good sign appears in the eastern sky.

		Your little boy tells you about it the next day.
		""")
	else:
		print("""
		The grasses so tremble...
		all the willows, their white flashes...
		upon the hillside, upon the fields...
		they besiege us so gently,
		they sway in repose.

		How could such beauty
		redouble your terror?
		""")
	
	if self["sorrow"] >= 10:
		print("""
		We have been so foolish.
		I have been so foolish.

		Can we be forgiven?
		
		Can we dedicate ourselves to reform?

		Or have we grown too weak
		to even muster the strength
		to recognize our own decadence
		and the necessity of tradition?
		""")
	if self["sorrow"] >= 5:
		print("""
		Nobody knows.

		Nothing matters.
		Nothing means anything.
	
		Let us free.
		""")
		grove["peace"] += 5
		self["peace"] += 5
	elif self["sorrow"] >= 2:
		print("""
		Let us free.
		Let us seek out
		some way of escape,
		let us get away from this.

		It's so foolish...
		just forgive us!
		We couldn't have known!
		""")
		grove["peace"] += 2
		self["peace"] += 2
	else:
		print("""
		No sentiment is required here.
		We will do what is necessary,
		and the superstitions of our forefathers
		will not hold back our progress.
		""")
		grove["anger"] += 5
		grove["determination"] += 5

	# finally determination

# NOW SET STAGE FOR DANCING
# The first dance is between the player
# and a single willow.
# The setting is a terrace on the 
# high part of the Marble City.
# The willows are pink in the distance
	return chars

def partTwo( chars ):
	self = chars["self"]
	citadel = chars["citadel"]
	grove = chars["grove"]


	print( """ 
	GUARDSMAN:
	Well NOW we know it's real!

	SCENE:
	The parapet surrounded.
	What use is armor?
	Shall we throw fire?

	From here, we can oversee
	the whole Westlands,
	the great Plains of Avinor,
	now fogged with marsh.
	
	And the song they bled,
	great trees out of the ancient lands
	grown wild beyond repair.

	They disassemble the parapet.
	They crush babies with stones.
	""" )
	raw_input()

	# Next some setup:

	# Setup the player
	playerEarth = 5
	playerAir = 5
	playerFire = 5
	playerWater = 5

	# Setup the tree
	willowEarth = 20
	willowAir = 10
	willowFire = 2
	willowWater = 20

	# There are two sides, the player and the willow.
	# Each receives a bonus equal to their side's share of
	# the three stats below.
	# Sorrow does not yet come into play.
	multiplier = 10
	totalDeterm = citadel["determination"] + self["determination"] + grove["determination"]
	totalPeace = citadel["peace"] + self["peace"] + grove["peace"]
	totalDeterm = citadel["anger"] + self["anger"] + grove["anger"]
	
	defenderDetermBonus = ( citadel["determination"] + self["determination"] ) / totalDeterm * multiplier
	defenderPeaceBonus = ( citadel["peace"] + self["peace"] ) / totalDeterm * multiplier
	defenderAngerBonus = ( citadel["anger"] + self["anger"] ) / totalDeterm * multiplier
	
	# Determination boosts Earth and Fire
	playerEarth += int(defenderDetermBonus)
	playerFire += int(defenderDetermBonus)
	
	# Peace boosts Water and Air
	playerWater += int(defenderPeaceBonus)
	playerAir += int(defenderPeaceBonus)
	
	# Anger boosts fire
	playerFire += int(defenderAngerBonus)
	
	# The willow receives the same bonuses, but mirrored.
	willowEarth += int( multiplier - defenderDetermBonus )
	willowFire += int( multiplier - defenderDetermBonus )
	willowFire += int( multiplier - defenderAngerBonus )
	willowWater += int( multiplier - defenderPeaceBonus )
	willowAir += int( multiplier - defenderPeaceBonus )
	
	if playerEarth > willowEarth:
		print("""
	The tree's bulk does not intimidate you.

	One might say it is willowy.
	""")

	if playerAir <= 10:
		print("""
	You hope this doesn't last too long.
		""")
	if playerAir <= 5:
		print("""
	You feel out of breath and anxious.
		""")

	if playerWater < willowWater:
		print("""
	The tree drinks from deep roots.
		""")
	if playerWater > willowWater:
		print("""
	Trees are things of peace.
		""")
	else:
		print("""
	The signs are fortuitous.
		""")

	if playerFire > willowFire:
		print("""
	You could probably overpower the tree.
		""")
		if playerWater > willowWater:
			print("""
		The it doesn't look too dangerous.
			""")
	elif playerFire < willowFire:
		print("""
	The tree's anger intimidates you.
		""")
		if playerWater == willowWater:
			print("""
		Yet the signs are good.
			""")

	# Use that info to create the dance object

	dance = rules.set_stage( 
			playerEarth, playerAir, playerFire, playerWater, # Player
			willowWater, willowAir, willowFire, willowWater, # Someday name a character WillowFire
			2, 0 ) # Start at mid-range
	gameData = json.loads( dance )
#	display.display( dance )

	dance = json.dumps( gameData )

	print( """
		This was autumn,
		and the leaves of the maples were yellow.
		The kingdom was white and amber that year;
		the sky was clear blue.
		And their white barks upon us,
		their twisting roots and their
		white whips of flower,
		they tore the stones from our walls
		and flung them down upon the city,
		brought the castle to earth,
		dissolved our entire architecture
		then besieged us here in the citadel.
		We defend it with fire-arrows.

		Your children are inside.
		Your brothers and sisters,
		your whole monstrous society:
		you have broken the covenant.

		They put an axe in your hand.
		Can you wield it?
		Can you wield it against the tree whose flesh
		is the flesh of your ancestors?

		""" )
	raw_input()

#	CHOICE TWO:

	def attack():
		"""
		Doing violence increases your own anger
		and the grove's.
		"""
		grove["anger"] += 2
		grove["peace"] -= 2
		self["anger"] += 1
		self["peace"] -= 2
	def holy():
		"""
		Holy behavior has a stranger effect.
		"""
		grove["sorrow"] += 2
		grove["peace"] += 1
		grove["determination"] -= 1
		self["peace"] += 2
		citadel["peace"] += 2
		citadel["sorrow"] += 1

	def checkDistance( distance ):
		"""
		Gives you information
		about how far the tree is.
		"""
		if distance == 0:
			print("""
		You are entangled in branches,
		actively wrestling and choking
		against great muscular trunks,
		struggling for survival.
			""")
		elif abs(distance) == 1:
			print("""
		The tree lashes you with its branches.
			""")
		else:
			print("""
		You are not very close to the tree.
			""")
	def checkBalance( bal0, bal1 ):
		"""
		Give information about relative balances,
		assuming bal0 is of the player,
		and prints an indication of one's chances.
		"""
		if abs(bal0) < abs(bal1):
			print("""
			You feel confident.
			""")
		elif abs(bal0) > abs(bal1):
			print("""
			Something doesn't feel right.
			""")
		else:
			print("""
			Things could go either way.
			""")
	def checkDeath():
		pass

	# INFORMATION:
	print( """
It roots up marble flagstones 
and heaves them through storefronts.

It crushes the homes of the living,
scatters their property all about.

It is the home of the dead.

You have a good steel axe in hand.
""")

	checkDistance( gameData["game"]["d"] )
	checkBalance( gameData["0"]["balance"], gameData["1"]["balance"] )
	
	# CHOICES:
	print("""
Do you advance upon it?
Do you shout out a prayer?
		""")

	answer = choose.choose( "advance", "shout" )

	# EFFECTS:
	if answer == "advance":
		print( """
	You advance purposefullly toward the willow,
	axe steady in your hand.

	It gazes sorrowfully at you.
	""" )
		grove["sorrow"] += 1
		gameData["0"]["choice"] = "advance"
	elif answer == "shout":
		print("""
	You shout out an urgent prayer:

	"Father! Have pity on me!
	Mother! Have pity on me!
	Honored grandfather,
	show me how I may be absolved!"

	The tree seems to glare at you.
	""")
		holy()
		gameData["0"]["choice"] = "jest"

	# RESPONSE:
	gameData["1"]["choice"] = "advance"
	if self["sorrow"] >= grove["sorrow"]:
		print( """
		The willow abandons its sad work
		and turns its attention to you.
		It trundles forwards,
		flaling its whips menacingly.
		""")
	else:
		print( """
	The willow flails its whips menacingly
	and advances upon you,
	crumbling marble with its feet.
	""")

	# INFORMATION
	if abs(gameData["0"]["balance"]) == abs(gameData["1"]["balance"]):
		print("""
	All things are in alignment.
	""")
	if abs(gameData["0"]["balance"]) < abs(gameData["1"]["balance"]):
		print("""
	What is to be feared?
	""")
	else:
		print("""
		What's wrong with me?
		""")

	if gameData["0"]["heat"] == gameData["0"]["fire"]:
		print("""
	Sweat upon your brow.
	You feel high.
	""")
		self["anger"] += 2
	raw_input()
	
	# TURN OVER THE GAME
	dance = json.dumps( gameData )
	dance = rules.turn( dance )
	gameData = json.loads( dance )
#	display.display( dance )

	# INFORMATION:
	checkDistance( gameData["game"]["d"] )
	checkBalance( gameData["0"]["balance"], gameData["1"]["balance"] )

	print("""
Do you chop at the tree's trunk?
Do you stand motionless before it?
Do you keep your distance?
""")
	answer = choose.choose( "chop", "stand", "distance" )

	# RESULTS:
	if answer == "chop":
		gameData["0"]["choice"] = "touch"
		print("""
		You raise your axe and swing with all your might.
	
		It bites deep into the limb.
		""")
		self["anger"] += 3
	elif answer == "stand":
		gameData["0"]["choice"] = "breathe"
		print("""
	You close your eyes and remain motionless.
	All thoughts leave your mind.
	""")
	elif answer == "distance":
		print("""
	You backpedal quickly,
	trying to stay out of its reach.
	""")
		gameData["0"]["choice"] = "retreat"
	else: raise Exception

	# IN RESPONSE, THE TREE WILL TOUCH.

	gameData["1"]["choice"] = "touch"

	# TURN OVER THE GAME
	dance = json.dumps( gameData )
	dance = rules.turn( dance )
	gameData = json.loads( dance )
#	display.display( dance )

	# INFORMATION
	if abs(gameData["game"]["d"]) < 2:
		print("""
		You're struck soundly by a branch,
		right in the gut,
		knocked to the ground,
		gasping for air.

		Dust rises around you.
		""")
	else:
		print("""
	The tree flails at you in rage.
	""")

	if gameData["0"]["heat"] == gameData["0"]["fire"]:
		print("""
	Your body is covered in cuts and bruises.
	""")

	if gameData["1"]["heat"] == gameData["1"]["fire"]:
		print("""
	You've made a fine start on that tree though.
	It looks like you could start
	to do some real damage soon.

	Maybe take off a limb.
	""")
	
	if gameData["0"]["heat"] == gameData["0"]["fire"]:
		print("""
		You feel dizzy.

		Can you keep this up?
		""")

	# CHOICE:

	checkDistance( gameData["game"]["d"] )
	checkBalance( gameData["0"]["balance"], gameData["1"]["balance"] )

	print("""
		Do you defend yourself?
		Or do you suddenly give voice to an ecstatic hymn?
		""")
	answer = choose.choose( "defend", "hymn" )

	# RESULT:
	if answer == "defend":
		if abs(gameData["game"]["d"]) > 1:
			if self["anger"] > 2:
				gameData["0"]["choice"] = "advance"
				print("""
			Sometimes the best defense
			is a good offence!
	
			You dive once again into the fray.
			People cheer from the balconies:
			their red & green silks,
			the marble balustrades,
			their golden bangles and ornaments.

			You swing your axe wildly to protect yourself.
			""")
			else:
				gameData["0"]["choice"] = "breathe"
				print("""
			Yet you feel in no danger.

			So you merely close your eyes
			and meditate upon the beauty of the universe.
			""")
			
		else:
			gameData["0"]["choice"] = "evade"
			print("""
		You manage to dodge a series of swiftly-swung branches.

		Gosh! That was close!
		""")
	elif answer == "hymn":
		gameData["0"]["choice"] = "jest"
		print("""
	Hao yumm ho hai!
	We bask the day away.
	Good tree, don't cry
	cause we forgot your
	ancient mystery,
	for TREE, we do love you
	& we sorrow for you.

	Please don't do us evil.
	Don't destroy our home.
	""")
		holy()
	else: raise Exception

	# IN RESPONSE, THE TREE WILL ADVANCE
	# This is the turning point.
	# If the player still has their faith after this,
	# The tree will back off.
	gameData["1"]["choice"] = "advance"
	print("""
		The tree closes in on you.
		""")

	print("""
		You have a sense of something
		heightened about the moment.
		""")

	# TURN THE GAME OVER
	dance = json.dumps( gameData )
	dance = rules.turn( dance )
	gameData = json.loads( dance )
#	display.display( dance )

	# INFORMATION:
	if gameData["game"]["d"] == 0 and gameData["0"]["choice"] != "evade":
		print("""
			The tree gives you a good knock in the head.
			""")
	else:
		print("""
	The willow thrashes
	its thin whips menacingly.

	It strews petals all about.
	""")

	if gameData["0"]["will"] < gameData["0"]["earth"]:
		print("""
	Your vision goes fuzzy for a second.
	You can feel your temple swelling
	and your brain pounding
	""")


	# CHOICE:

	checkDistance( gameData["game"]["d"] )
	checkBalance( gameData["0"]["balance"], gameData["1"]["balance"] )

	if gameData["1"]["heat"] == gameData["1"]["fire"]:
		print("""
		The bark is shorn from its limb.
		""")

	print("""
		Do you strike once again?
		Do you give yourself up to the tree's will?
		Or do you try to flee?
		""")
	answer = choose.choose( "strike", "drift", "flee" )
	# Poor lads don't have command lines
	if answer == "strike":
		gameData["0"]["choice"] = "touch"
		print("""
	You swing your axe in a great arc.
	""")
		attack()
		
		# Note the quality of the blow
		if abs(gameData["0"]["balance"]) < abs(gameData["1"]["balance"]):
			print("""
		You deal it a mighty blow!
		""")
		if abs(gameData["0"]["balance"]) == abs(gameData["1"]["balance"]):
			print("""
		The terrace echoes
		with the sound of your strike.
		""")
		if abs(gameData["0"]["balance"]) > abs(gameData["1"]["balance"]):
			print("""
		It's not a direct hit.
		""")
		
		# Then tell if real damage has been dealt.
		if gameData["1"]["will"] < gameData["1"]["earth"]:
			print("""
			You have lopped off a great limb!
			It falls you the ground!

			This will make a fine trophy.
			""")


	elif answer == "drift":
		gameData["0"]["choice"] = "breathe"
		print("""
	You collapse into the tree's embrace.
	""")
		holy()
	elif answer == "flee":
		gameData["0"]["choice"] = "retreat"
		if abs(gameData["game"]["d"]) == 0:
			print("""
		You disentangle yourself
		and slip out of the grasp
		of twining tendrils.
		""")
		else:
			print("""
		You back further away.
		""")
	else: raise Exception

	# IN RESPONSE, THE TREE WILL JUDGE YOU
	def judge( gameData ):
		if (gameData["1"]["heat"] < gameData["1"]["fire"]) and (gameData["0"]["calm"] >= gameData["1"]["calm"]):
			return True
		elif self["peace"] >= grove["peace"] and gameData["0"]["calm"] >= gameData["1"]["calm"]:
			return True
		else: return False

	if judge( gameData ):
		gameData["1"]["choice"] = "breathe"
		gameData["1"]["will"] = 0
		grove["peace"] += 5
		grove["anger"] -= 5
		print( """
The tree suddenly relaxes.
It seems to expand,
and sparkle in the sunlight.

You have brought it to peace.
""")
	else:
		gameData["1"]["choice"] = "touch"
		print( """
	The tree rages and thrashes its mighty branches.
	""")

	dance = json.dumps( gameData )
	dance = rules.turn( dance )
	display.display( dance )
	gameData = json.loads( dance )
#	display.display( dance )
	
	if abs(gameData["game"]["d"]) <= 1:
		print("""
		You are badly wounded,
		and later wake up in the infirmary.
		""")
	else:
		print("""
		You manage to get away,
		and return to the citadel
		to give word of your mission.
		""")
# EPODE
# Wrap up the chapter by turning dance data back into real data

# If your heat is greater than the tree's,
# you may have walked a path of power.
	if gameData["0"]["heat"] > gameData["1"]["heat"]:
		print( """
		Now THIS will show your worth!
		""")
	
	if gameData["1"]["will"] < gameData["1"]["earth"]:
		print("""
		They tell you the tree has retreated!
		""")

	# If your calm is greater than the tree's,
	# You may have walked a path of peace.
	if gameData["0"]["calm"] > gameData["1"]["calm"]:
		print("""
		You have navigated the situation
		with grace and beauty.
		""")
		if abs(gameData["0"]["balance"]) < abs(gameData["1"]["balance"]):
			print("""
			Even the tree is in awe of you.
			""")
		if gameData["1"]["will"] < gameData["1"]["earth"]:
			print("""
			They will sing of this day for ages.
			""")
		if gameData["0"]["will"] < gameData["0"]["earth"]:
			print("""
			You have sacrificed much,
			and you will sacrifice again.
			""")
	elif gameData["0"]["calm"] > gameData["1"]["calm"]:
		print("""
		And yet the grove is so beautiful.
		""")
	else:
		print("""
		A fair omen shines in the east.
		""")


	# If you have taken will damage, determination is reduced.
	if gameData["0"]["will"] * 2 < gameData["0"]["earth"]:
		print("""
		You have been gravely wounded.

		They looked at you for a while
		as if you were already dead.

		Now they watch you with hope and fear.
		""")
		self["determination"] -= 5
		self["anger"] += 3
		citadel["anger"] += 7
	elif gameData["0"]["will"] < gameData["0"]["earth"]:
		print("""
		The experience has taken a toll on you.
	
		People stare at your wounds.
		""")
		self["determination"] -= 2
		self["anger"] += 2
		citadel["anger"] += 5
	
	# If the tree hasn't taken will damage, the citadel is harmed.
	if gameData["1"]["calm"] == gameData["1"]["air"]:
		# Unless it has been calmed.
		grove["peace"] += 3
		grove["determination"] -= 3
		print("""
		The tree seems to smile upon you.
		""")
	elif gameData["1"]["will"] == gameData["1"]["earth"]:
		citadel["determination"] -= 5
		print("""
		The tree is grim toward you.
		""")
	else:
		# Your violence makes you feel guilty
		# But the forest's determination is dulled.
		self["sorrow"] += 5
		print("""
		You regret your brutal and heretical acts.
		""")

	print( "self" )
	print( self )
	print( "grove" )
	print( grove )
	print( "citadel" )
	print( citadel )
	
	return chars

# This section includes no choices,
# but tells you the result of your actions.
def epilogue( chars ):
	self = chars["self"]
	citadel = chars["citadel"]
	grove = chars["grove"]

	# See who is more determined between attacker and defender.
	defenderDeterm = self["determination"] + citadel["determination"]
	if defenderDeterm > grove["determination"]:
		print("""
	You are probably able to overpower this foe.
		""")
	elif defenderDeterm < grove["determination"]:
		print("""
	The enemy weighs heavily upon you
	and your family is full of fear.
		""")
	else:
		print("""
	The tests ahead will be desperate.
	You must be careful.
		""")

	# Warn the player if they are weak
	if self["determination"] <= 2:
		print("""
	You aren't sure you can continue.
		""")
	if self["determination"] <= 5:
		print("""
	Your wounds are many.
		""")
	if self["determination"] < 10:
		print("""
	Your resolve is wavering.
		""")
	if self["determination"] == 10:
		print("""
	You feel fine.
		""")
	if self["determination"] > 10:
		print("""
	You feel your triumph assured.
		""")

	# Let the player know if they have more determination than the grove.
	# This might be impossible.
	if self["determination"] > grove["determination"]:
		print("""
	You feel up to the challenge.
		""")

	# Next test anger.
	if grove["anger"] > self["anger"] * 3:
		print("""
		The fury of the grove
		fills you with trembling.

		The air vibrates with its hatred.
		""")
	elif grove["anger"] > self["anger"]:
		print("""
		You fear they will never forgive you.
		""")
	elif self["anger"] > grove["anger"]:
		print("""
	Waving willow tendrils
	in golden air
	seem to mock you.
		""")
		grove["peace"] -= 5
		grove["determination"] += 5
		grive["sorrow"] -= 1
	else:
		print("""
	Two fires
	may rage as one.
		""")

	# Sorrow is admirable, in this case.
	if self["sorrow"] + citadel["sorrow"] >= 20:
		print("""
	Some say the grove
	has made note of the honor
	and the willingness to repent
	in the people of the city.
		""")
		grove["determination"] -= 5
	elif self["sorrow"] + citadel["sorrow"] >= 10:
		print("""
	The city weeps and mourns.
		""")

	# peace is always good
	if self["peace"] > grove["peace"]:
		print("""
	You watch the trees
	sparkle in the wind
	and you feel that they love you.	
		""")
		grove["peace"] += 10
		grove["anger"] -= 5
		grove["determination"] -= 5
	elif self["peace"] < grove["peace"]:
		print("""
	And yet the trees are still so beautiful to you.
		""")
		self["peace"] += 5
		self["sorrow"] += 1
	else:
		print("""
	Tales reach you
	of a strange birth in the distant west.
		""")

	if self["peace"] > citadel["peace"]:
		citadel["peace"] += 1
	else:
		self["anger"] -= 1

	# The citadel's will to continue
	# is essential to a good final ending.
	if citadel["determination"] >= 10:
		print("""
	The citadel is still secure.
	The people are anxious.
		""")
	elif citadel["determination"] >= 5:
		print("""
	Many people have died.

	The situation seems dire.
		""")
	return chars

def start():
	chars = intro()
	chars = partOne( chars )
	chars = partTwo( chars )
	chars = epilogue( chars )

# CHAPTER TWO
## The Willow at Night

# CHAPTER THREE
## The Great Council

# CHAPTER FOUR
## The Great Sally

# CHAPTER FIVE
## Distant Future Wedding Dance

