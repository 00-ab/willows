import curses
import json
import pprint

TABLE_SYM_ONE = "I"
TABLE_SYM_TWO = "*"
TABLE_WIDTH = 41
TABLE_HEIGHT = 9
TABLE_COL_ONE = 20


def display( game ):
	"""
	Accepts a dance-game JSON object
	and passes it through the wrapper to _display,
	which does the real drawing.
	"""
	game = curses.wrapper( _display, game )
	return game

def _display( win, game0 ):
	stdscr = win
	game_data = json.loads( game0 )
	
	curses.init_pair( 1, curses.COLOR_RED, curses.COLOR_BLACK )
	curses.init_pair( 2, curses.COLOR_RED, curses.COLOR_BLACK )
	curses.init_pair( 3, curses.COLOR_RED, curses.COLOR_BLACK )
	curses.init_pair( 4, curses.COLOR_RED, curses.COLOR_BLACK )
	
	choice = None
	while( choice != 'q' ):
	
		_print_stats( stdscr, 1, 1, "PLAYER ONE", game_data['0'] )
		_print_stats( stdscr, 1, 51, "PLAYER TWO", game_data['1'])

		# insert map display here

		strng = "Turn " + str(game_data['game']['turn']) + ". Press any key."
		win.addstr( curses.LINES-1, 1, strng )
		win.getch()
		for x in range(curses.COLS-1):
			win.addch( curses.LINES-1, x, " " )
		
		# Get inputs
		win.addstr( curses.LINES-1, 1, "Player Zero, input move. " )
		choice = chr( win.getch() )
		game_data["0choice"] = choice
		for x in range(curses.COLS-1):
			win.addch( curses.LINES-1, x, " " )

		win.addstr( curses.LINES-1, 1, "Player One, input move. " )
		choice = chr( win.getch() )
		game_data["1choice"] = choice
		for x in range(curses.COLS-1):
			win.addch( curses.LINES-1, x, " " )
	
	game1 = json.dumps( game_data )
	return game1
		

def _print_stats( win, y, x, title, player ):
	d = json.dumps( player )
	win.addstr( y, x+1, title )

	# Draw the border of the dable
	win.vline( y+1, x, TABLE_SYM_TWO, TABLE_HEIGHT )
	win.vline( y+1, x+TABLE_COL_ONE, TABLE_SYM_TWO, TABLE_HEIGHT )
	win.vline( y+1, x-1+TABLE_WIDTH, TABLE_SYM_TWO, TABLE_HEIGHT )

	win.hline( y+1, x, TABLE_SYM_ONE, TABLE_WIDTH )
	win.hline( y+3, x, TABLE_SYM_ONE, TABLE_WIDTH )
	win.hline( y+5, x, TABLE_SYM_ONE, TABLE_WIDTH )
	win.hline( y+7, x, TABLE_SYM_ONE, TABLE_WIDTH )
	win.hline( y+9, x, TABLE_SYM_ONE, TABLE_WIDTH )

	# Print the information
	win.addstr( y+2, x+2, 'EARTH/WILL' )
	win.addstr( y+4, x+2, 'AIR/CALM' )
	win.addstr( y+6, x+2, 'FIRE/PASSION' )
	win.addstr( y+8, x+2, 'WATER/BALANCE' )
	
	strng = "{0}/{1}".format(player['earth'], player['will'] )
	win.addstr( y+2, x+2+TABLE_COL_ONE, strng )

	strng = "{0}/{1}".format(player['air'], player['calm'] )
	win.addstr( y+4, x+2+TABLE_COL_ONE, strng )

	strng = "{0}/{1}".format(player['fire'], player['heat'] )
	win.addstr( y+6, x+2+TABLE_COL_ONE, strng )
	
	strng = "{0}/{1}".format(player['water'], player['balance'] )
	win.addstr( y+8, x+2+TABLE_COL_ONE, strng )
		
if __name__ == '__main__':
	curses.wrapper(_display, game_temp)
