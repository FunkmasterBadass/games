import gamestate
from lib.characters import *
from settings import Settings

if __name__ == "__main__":
	state = gamestate.GameState([Villager('test0'), Villager('test1'), Doctor('test2'), Cop('test3'), Mafia('test4')], Settings())
	state.run()