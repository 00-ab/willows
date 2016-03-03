def narrate( script ):
	for line in script:
		if line[0:1] == "# ":
			parse( line )

def parse( line ):
	flag = line[2:]

	# now I'm not sure if the scripts should be .txt or .py...
