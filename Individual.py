import json
import requests
import random as rd


from classes.next_game import NextGame
from classes.player import Player
from classes.positions import Position
from classes.status import Status
from classes.team import Team

# TODO LISTA DE PLAYERS TEM Q SER TIPADA


class Individual:
    __players: list[Player]
    __next_games: list[NextGame]
    __teams: list[Team]
    __positions: list[Position]
    __status: list[Status]
    __fitness: float
    size: int

    def __init__(self, individual_population=[]):
        self.__next_games, self.__players, self.__teams, self.__positions, self.__status = self.__get_info()
        self.__individual_population = individual_population
        self.size = len(self.__players)
        self.__fitness = -99999

    def get_team_fitness(self) -> float:
        return self.__fitness

    @staticmethod
    def __get_info() -> list[list[NextGame], list[Player], list[Team], list[Position], list[Status]]:
        next_games_response = requests.get(
            'https://api.cartola.globo.com/partidas')
        market_response = requests.get(
            'https://api.cartola.globo.com/atletas/mercado')

        if next_games_response.status_code != 200 or market_response.status_code != 200:
            raise Exception("Erro na req da api")

        next_games_json = json.loads(next_games_response.content)
        market_json = json.loads(market_response.content)

        if market_json == {} or next_games_json == {}:
            raise Exception("Erro na res da api")

        next_games_list = next_games_json['partidas']
        teams_list = market_json['clubes']
        positions_list = market_json['posicoes']
        status_list = market_json['status']
        players_list = market_json['atletas']

        teams: list[Team] = []
        positions: list[Position] = []
        status: list[Status] = []
        next_games: list[NextGame] = []
        players: list[Player] = []

        for team in teams_list:
            t = Team(teams_list[team])
            teams.append(t)

        for position in positions_list:
            p = Position(positions_list[position])
            positions.append(p)

        for status_aux in status_list:
            s = Status(status_list[status_aux])
            status.append(s)

        for next_game in next_games_list:
            n = NextGame(next_game)
            next_games.append(n)

        for player in players_list:
            pl = Player(player)
            players.append(pl)

        return [next_games, players, teams, positions, status]

    def get_individual_population(self) -> list:
        return self.__individual_population

    def get_player(self, index: int) -> Player or None:
        if index > len(self.__players):
            return None

        return self.__players[index]

    def get_players(self) -> list[Player]:
        return self.__players

    def get_individual_len(self) -> int:
        return len(self.__individual_population)

    def get_next_matches(self):
        return self.__next_games

    def get_player_by_name(self, name: str) -> Player or None:
        for player in self.__players:
            if name in player.apelido:
                return player
        return None

    def get_team_by_id(self, id: str):
        for team_id in self.__teams:
            if team_id == id:
                return self.__teams[team_id]
        return None

    def generate_solution(self) -> None:
        ready = False
        count = 0
        what_need = {
            1: 1,  # goleiro
            2: 2,  # lateral
            3: 2,  # zagueiro
            4: 3,  # meia
            5: 3,  # atacante
            6: 1,  # tecnico
        }
        what_already_have = {
            1: 0,  # goleiro
            2: 0,  # lateral
            3: 0,  # zagueiro
            4: 0,  # meia
            5: 0,  # atacante
            6: 0,  # tecnico

        }

        # insert 0 to list
        for _ in self.__players:
            self.__individual_population.append(0)

        # change random indexes to 1, randomize population
        while not ready:
            random_number = rd.randrange(0, len(self.__players))
            player = self.__players[random_number]
            will_add = True if what_already_have.get(player.posicao_id) < what_need.get(
                player.posicao_id) else False

            if will_add:
                what_need[player.posicao_id] -= 1
                count += 1
                self.__individual_population[random_number] = 1

            ready = True if count >= 12 else False

    def get_individual_fitness(self, budget: int):
        team_budget = 0
        team_members = []
        fitness_of_team_members = 0

        for index, player in enumerate(self.__individual_population):
            if player == 1:
                team_budget += self.__players[index].preco_num
                team_members.append(index)

        if team_budget > budget:
            return 0, 0

        # for each player that is in this team
        for index in team_members:
            player_team, opposing_team = self.get_teams_by_player(
                self.__players[index])

            if player_team is not None:
                fitness_of_team_members += self.__is_player_team_better(
                    self.__players[index])
                fitness_of_team_members += self.__is_player_playing_at_home(
                    self.__players[index])
                fitness_of_team_members += self.__is_player_team_with_best_performance(
                    self.__players[index])
                fitness_of_team_members += self.__get_player_points(
                    self.__players[index])

        self.__fitness = fitness_of_team_members

        return fitness_of_team_members, team_budget

    def get_teams_by_player(self, player: Player):
        players_team_id = player.clube_id
        player_team, opposing_team = None, None

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                player_team = match['clube_casa_id']
                opposing_team = match['clube_visitante_id']
            elif match['clube_visitante_id'] == players_team_id:
                player_team = match['clube_visitante_id']
                opposing_team = match['clube_casa_id']

        return player_team, opposing_team

    def __is_player_team_better(self, player: Player):
        players_team_id = player.clube_id
        player_team_position, opposing_team_position = -1, -1

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                player_team_position = match['clube_casa_posicao']
                opposing_team_position = match['clube_visitante_posicao']
            elif match['clube_visitante_id'] == players_team_id:
                player_team_position = match['clube_visitante_posicao']
                opposing_team_position = match['clube_casa_posicao']

            return 1 if player_team_position < opposing_team_position else 0

    def __is_player_playing_at_home(self, player: Player):
        players_team_id = player.clube_id
        is_playing_at_home = -1

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                is_playing_at_home = 1
            elif match['clube_visitante_id'] == players_team_id:
                is_playing_at_home = 0

        return is_playing_at_home

    def __handle_player_points(self, players_performance: str, opposing_performance: str, player_points: int) -> int:
        points = player_points

        if players_performance == 'v':
            if opposing_performance == 'd':
                points += 2
            elif opposing_performance == 'e':
                points += 1

        elif players_performance == 'd':
            if opposing_performance == 'v':
                points -= 2
            elif opposing_performance == 'e':
                points -= 1

        elif players_performance == 'e':
            if opposing_performance == 'v':
                points -= 1
            elif opposing_performance == 'd':
                points += 1

        return points

    def __is_player_team_with_best_performance(self, player: Player) -> int:
        players_team_id = player.clube_id
        players_team_performance, opposing_team_performance = [], []

        # return players' team performance against opposing team performance
        player_points = 0

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                players_team_performance = match['aproveitamento_mandante']
                opposing_team_performance = match['aproveitamento_visitante']
            elif match['clube_visitante_id'] == players_team_id:
                players_team_performance = match['aproveitamento_visitante']
                opposing_team_performance = match['aproveitamento_mandante']

        if len(players_team_performance) != 0:
            for idx in range(len(players_team_performance)):
                player_points = self.__handle_player_points(
                    players_team_performance[idx], opposing_team_performance[idx], player_points)

        return player_points

    def __get_player_points(self, player: Player) -> int:
        if player.preco_num == 0 or player.media_num == 0 or player.minimo_para_valorizar == 0:
            return 0

        player_price_valorize_bool = 1 if int(
            player.preco_num / player.media_num) < (player.minimo_para_valorizar or 0) else 0
        player_overpriced_bool = 1 if player.preco_num / player.media_num > 2 else 0
        return player_price_valorize_bool + player_overpriced_bool
