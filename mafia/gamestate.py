from settings import Settings
from utilities import Timer
from lib.constants import *
import asyncio

def GameState():

    def __init__(players: list):
        self.is_day = Settings.start_day
        self.day_time = Settings.day_time
        self.night_time = Settings.night_time
        self.hide_roles_on_death = Settings.hide_roles_on_death
        self.players = players
        self.ability_players = [p if p.has_ability() for p in players]
        self.alive_players = [p if p.is_alive() for p in players]
        self.total_votes = 0
        self.timer_completed = False

    async def get_player(msg):
        # need to implement
        pass

    async def timer_callback():
        await asyncio.sleep(0.1)
        self.timer_completed = True

    async def prompt_player(player):
        if self.is_day:
            msg = 'Select a player:\n'
            player_index = None
            for idx, p in enumerated(self.alive_players):
                if p == player:
                    player_index = idx
                msg = f'{msg}[{idx}] {player.name}\n'
            self.alive_players[get_player(msg)].vote()
        else:
            if player.get_ability() == ABILITY_MAFIA:
                pass
            elif player.get_ability() == ABILITY_DOCTOR:
                pass
            elif player.get_ability() == ABILITY_COP:
                pass
            elif player.get_ability() == ABILITY_NONE:
                pass
            else:
                print("how'd you get here?")
        self.total_votes += 1

    async def main():
        self.timer_completed = False
        self.total_votes = 0
        self.alive_players = [p if p.is_alive() for p in self.players]
        mafia_members = [p if p.is_mafia_aligned() for p in self.alive_players]
        town_members = [p if p.is_town_aligned() for p in self.alive_players]
        if len(mafia_members) >= len(town_members):
            print('Mafia wins!')
        elif len(mafia_members) == 0:
            print('Town wins!')
        if self.is_day:
            seconds = self.day_time*60
            players_to_prompt = self.alive_players
            votes_required = (len(players_to_prompt) // 2) + 1
        else:
            seconds = self.night_time*60
            players_to_prompt = [p if p.is_alive() for p in self.ability_players]
            votes_required = len(players_to_prompt)
        timer = Timer(seconds, callback)
        for player in players_to_prompt:
            prompt_player(player)
        while self.total_votes != votes_required:
            if self.timer_completed:
                break
        if self.is_day:
            nominated = (0, None)
            for player in self.alive_players:
                if player.death_votes > nominated[0]
                    nominated = (player.death_votes, player)
            if nominated[0] >= votes_required and nominated[1] is not None:
                print(f'{player} has been killed by town!')
                nominated[1].die()
        else:
