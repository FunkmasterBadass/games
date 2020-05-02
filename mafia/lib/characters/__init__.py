from lib.constants import *

def Villager():

	def __init__(player, alignment=ALIGNMENT_TOWN, ability=ABILITY_NONE):
		self._player = player
		self._alignment = alignment
		self._ability = ability
		self._alive = True
		self.health = 1
		self.death_votes = 0

	def vote():
		self.death_votes += 1

	def survive():
		self.death_votes = 0

	def die():
		self._alive = False

	def get_ability():
		return self._ability

	def has_ability():
		return self._ability != ABILITY_NONE

	def is_alive():
		return self._alive

	def is_mafia_aligned():
		return self._alignment = ALIGNMENT_MAFIA

	def is_town_aligned():
		return self._alignment = ALIGNMENT_TOWN

def Mafia(Villager):

	def __init__(player):
		super().__init__(player=player, alignment=ALIGNMENT_MAFIA, ability=ABILITY_MAFIA)


def Doctor(Villager):

	def __init__(player):
		super().__init__(player=player, alignment=ALIGNMENT_TOWN, ability=ABILITY_DOCTOR)


def Cop(Villager):

	def __init__(player):
		super().__init__(player=player, alignment=ALIGNMENT_TOWN, ability=ABILITY_COP)
