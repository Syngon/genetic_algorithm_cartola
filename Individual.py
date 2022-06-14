import pandas as pd
import random as rd
from random import randint
import requests
import matplotlib.pyplot as plt
import json


class Individual:
    def __init__(self):
        self.__next_games, self.__players, self.__teams, self.__positions, self.__status = self.get_info()
        self.__individual_population = []

    @staticmethod
    def get_info():
        next_games_response = requests.get('https://api.cartola.globo.com/partidas')
        market_response = requests.get('https://api.cartola.globo.com/atletas/mercado')

        if next_games_response.status_code != 200 or market_response.status_code != 200:
            raise Exception("Erro na req da api")

        next_games_json = json.loads(next_games_response.content)
        market_json = json.loads(market_response.content)

        if market_json == {} or next_games_json == {}:
            raise Exception("Erro na res da api")

        next_games = next_games_json['partidas']
        teams = market_json['clubes']
        positions = market_json['posicoes']
        status = market_json['status']
        players = market_json['atletas']

        return next_games, players, teams, positions, status

    def get_individual_population(self):
        return self.__individual_population

    def get_players(self):
        return self.__players

    def get_individual_len(self):
        return len(self.__individual_population)

    def get_next_matches(self):
        return self.__next_games

    def get_player_by_name(self, name):
        for player in self.__players:
            if name in player['apelido']:
                return player
        return None

    def get_team_by_id(self, id):
        for team_id in self.__teams:
            if team_id == str(id):
                return self.__teams[team_id]
        return None

    def generate_solution(self):
        is_ready = False
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
        while is_ready is False:
            random_number = rd.randrange(0, len(self.__players))
            player = self.__players[random_number]
            will_add = True if what_already_have.get(player['posicao_id']) < what_need.get(
                player['posicao_id']) else False

            if will_add:
                what_need[player['posicao_id']] -= 1
                count += 1
                self.__individual_population[random_number] = 1

            is_ready = True if count >= 12 else False

        return True

    def get_individual_fitness(self, budget):
        team_budget = 0
        team_members = []
        fitness_of_team_members = 0

        for index, player in enumerate(self.__individual_population):
            if player == 1:
                team_budget += self.__players[index]['preco_num']
                team_members.append(index)

        if team_budget > budget:
            return 0

        # for each player that is in this team
        for index in team_members:
            player_team, opposing_team = self.get_teams_by_player(self.__players[index])

            if player_team is not None:
                fitness_of_team_members += self.is_player_team_better(self.__players[index])
                fitness_of_team_members += self.is_player_playing_at_home(self.__players[index])
                fitness_of_team_members += self.is_player_team_with_best_performance(self.__players[index])
                fitness_of_team_members += self.get_player_points(self.__players[index])

        return fitness_of_team_members, team_budget


    def get_teams_by_player(self, player):
        players_team_id = player['clube_id']
        player_team, opposing_team = None, None

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                player_team = match['clube_casa_id']
                opposing_team = match['clube_visitante_id']
            elif match['clube_visitante_id'] == players_team_id:
                player_team = match['clube_visitante_id']
                opposing_team = match['clube_casa_id']

        return player_team, opposing_team

    def is_player_team_better(self, player):
        players_team_id = player['clube_id']
        player_team_position, opposing_team_position = -1, -1

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                player_team_position = match['clube_casa_posicao']
                opposing_team_position = match['clube_visitante_posicao']
            elif match['clube_visitante_id'] == players_team_id:
                player_team_position = match['clube_visitante_posicao']
                opposing_team_position = match['clube_casa_posicao']

            return 1 if player_team_position < opposing_team_position else 0

    def is_player_playing_at_home(self, player):
        players_team_id = player['clube_id']
        is_playing_at_home = -1

        for match in self.__next_games:
            if match['clube_casa_id'] == players_team_id:
                is_playing_at_home = 1
            elif match['clube_visitante_id'] == players_team_id:
                is_playing_at_home = 0

        return is_playing_at_home

    def is_player_team_with_best_performance(self, player):
        players_team_id = player['clube_id']
        players_team_performance, opposing_team_performance = [], []

        #return players' team performance against opposing team performance
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
                if players_team_performance[idx] == 'v':
                    if opposing_team_performance[idx] == 'd':
                        player_points += 2
                    elif opposing_team_performance[idx] == 'e':
                        player_points += 1

                elif players_team_performance[idx] == 'd':
                    if opposing_team_performance[idx] == 'v':
                        player_points -= 2
                    elif opposing_team_performance[idx] == 'e':
                        player_points -= 1

                elif players_team_performance[idx] == 'e':
                    if opposing_team_performance[idx] == 'v':
                        player_points -= 1
                    elif opposing_team_performance[idx] == 'd':
                        player_points += 1

        return player_points

    def get_player_points(self, player):
        if player['preco_num'] == 0 or player['media_num'] == 0 or player['minimo_para_valorizar'] :
            return 0

        player_price_valorize_bool = 1 if player['preco_num'] / player['media_num'] < player['minimo_para_valorizar'] else 0
        player_overpriced_bool = 1 if player['preco_num'] / player['media_num'] > 2 else 0
        return player_price_valorize_bool + player_overpriced_bool







