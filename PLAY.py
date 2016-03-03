import glob # First get a list of all story modules.
import imp

stories = glob.glob( './stories/*.py' )

print("""


   _-~-:: Welcome to Dance ::-~-_


Select your story:

""")

# Print the story options.
for s in enumerate(stories):
	strng = " {0} : {1}".format( s[0], s[1] )
	print( strng )

choice = raw_input( "Enter a number: " )
story = imp.load_source( 'story', stories[ int(choice) ] )

story.start()
