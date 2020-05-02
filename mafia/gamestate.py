from utilities import Timer
from lib.constants import *
import asyncio

class GameState():

    def __init__(self, players: list, settings):
        self.is_day = settings.start_day
        self.day_time = settings.day_time
        self.night_time = settings.night_time
        self.hide_roles_on_death = settings.hide_roles_on_death
        self.players = players
        self.ability_players = [p for p in self.players if p.has_ability()]
        self.alive_players = [p for p in self.players if p.is_alive()]
        self.total_votes = 0
        self.timer_completed = False
        self.game_over = False

    def send_msg(self, player, msg):
        # need to implement
        print(msg)

    def get_player(self, player, msg):
        # need to implement
        return 0

    async def callback(self):
        await asyncio.sleep(0.1)
        print('timer completed')
        self.timer_completed = True

    async def prompt_player(self, player):
        await asyncio.sleep(0.1)
        if self.is_day:
            msg = 'Select a player to vote off:\n'
            player_index = None
            for idx, p in enumerate(self.alive_players):
                if p == player:
                    player_index = idx
                msg = f'{msg}[{idx}] {player}\n'
            self.alive_players[self.get_player(player, msg)].vote()
        else:
            if player.get_ability() == ABILITY_MAFIA:
                msg = 'Select a player to kill:\n'
                player_index = None
                for idx, p in enumerate(self.alive_players):
                    if p == player:
                        player_index = idx
                    msg = f'{msg}[{idx}] {player}\n'
                self.alive_players[self.get_player(player, msg)].hit()
            elif player.get_ability() == ABILITY_DOCTOR:
                msg = 'Select a player to save:\n'
                player_index = None
                for idx, p in enumerate(self.alive_players):
                    if p == player:
                        player_index = idx
                    msg = f'{msg}[{idx}] {player}\n'
                self.alive_players[self.get_player(player, msg)].save()
            elif player.get_ability() == ABILITY_COP:
                msg = 'Select a player to check:\n'
                player_index = None
                for idx, p in enumerate(self.alive_players):
                    if p == player:
                        player_index = idx
                    msg = f'{msg}[{idx}] {player}\n'
                selected_player = self.alive_players[self.get_player(player, msg)]
                if selected_player.is_mafia_aligned():
                    self.send_msg(player, f'{selected_player} IS Mafia!')
                else:
                    self.send_msg(player, f'{selected_player} IS NOT Mafia!')
            else:
                pass
        self.total_votes += 1

    async def main(self):
        self.timer_completed = False
        self.total_votes = 0
        self.alive_players = [p for p in self.alive_players if p.is_alive()]
        mafia_members = [p for p in self.alive_players if p.is_mafia_aligned()]
        town_members = [p for p in self.alive_players if p.is_town_aligned()]
        if len(mafia_members) >= len(town_members):
            print('Mafia wins!')
            self.game_over = True
            return
        elif len(mafia_members) == 0:
            print('Town wins!')
            self.game_over = True
            return
        if self.is_day:
            print("Day time, begin!")
            seconds = self.day_time*60
            players_to_prompt = self.alive_players
            votes_required = (len(players_to_prompt) // 2) + 1
        else:
            print("Night time, begin!")
            seconds = self.night_time*60
            players_to_prompt = [p for p in self.ability_players if p.is_alive()]
            votes_required = len(players_to_prompt)
        timer = Timer(seconds, self.callback)
        tasks = []
        for player in players_to_prompt:
            task = asyncio.ensure_future(self.prompt_player(player))
            tasks.append(task)
        tasks = asyncio.gather(*tasks)
        await tasks

        while self.total_votes < len(players_to_prompt):
            if self.timer_completed:
                break
        if not self.timer_completed:
            timer.cancel()
        if self.is_day:
            nominated = (0, None)
            for idx, player in enumerate(self.alive_players):
                if player.death_votes > nominated[0]:
                    nominated = (player.death_votes, idx)
            if nominated[0] >= votes_required and nominated[1] is not None:
                idx = nominated[1]
                print(f'{self.alive_players[idx]} has been killed by town!')
                self.alive_players[idx].die()
            print("Day time, end!")
            self.is_day = False
        else:
            for player in self.alive_players:
                if player.should_die():
                    print(f'{player} has been killed!')
                    player.die()
            print("Night time, end!")
            self.is_day = True
        self.alive_players = [p for p in self.alive_players if p.is_alive()]
        for player in self.alive_players:
            player.reset_flags()
            player.survive()

    def run(self):
        while not self.game_over:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.main())
            finally:
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.close()