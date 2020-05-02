from lib.constants import *

class Villager():

	def __init__(self, player, alignment=ALIGNMENT_TOWN, ability=ABILITY_NONE):
		self._player = player
		self._alignment = alignment
		self._ability = ability
		self._alive = True
		self.doctor_buff = False
		self.death_flag = False
		self.death_votes = 0

	def __repr__(self):
		return self._player

	def vote(self):
		self.death_votes += 1

	def survive(self):
		self.death_votes = 0

	def hit(self):
		self.death_flag = True

	def die(self):
		self._alive = False

	def get_ability(self):
		return self._ability

	def has_ability(self):
		return self._ability != ABILITY_NONE

	def is_alive(self):
		return self._alive

	def is_mafia_aligned(self):
		return self._alignment == ALIGNMENT_MAFIA

	def is_town_aligned(self):
		return self._alignment == ALIGNMENT_TOWN

	def save(self):
		self.doctor_buff = True

	def should_die(self):
		return self.death_flag and not self.doctor_buff

	def reset_flags(self):
		self.doctor_buff = False
		self.death_flag = False

class Mafia(Villager):

	def __init__(self, player):
		super().__init__(player=player, alignment=ALIGNMENT_MAFIA, ability=ABILITY_MAFIA)


class Doctor(Villager):

	def __init__(self, player):
		super().__init__(player=player, alignment=ALIGNMENT_TOWN, ability=ABILITY_DOCTOR)


class Cop(Villager):

	def __init__(self, player):
		super().__init__(player=player, alignment=ALIGNMENT_TOWN, ability=ABILITY_COP)
