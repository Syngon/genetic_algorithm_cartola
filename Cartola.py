import random
from turtle import position
import numpy as np
import pandas as pd
import random as rd
from random import randint
import requests
import matplotlib.pyplot as plt
import json

from Individual import Individual

# TODO MELHORAR FUNC FITNESS



# TODO SELECTION PRA FRENTE


# Has the responsability to manage individuals
class Cartola:
    def __init__(self, budget, num_generations=150, solutions_per_pop=8):
        self.budget = budget
        self.num_generations = num_generations
        self.solutions_per_pop = solutions_per_pop
        self.population = self.get_initial_population()
        self.pop_size = (self.solutions_per_pop, self.population[0].get_individual_len())

    def optimize(self):
        parameters, fitness_history, team_budget_history = [], [], []
        num_parents = int(self.pop_size[0] / 2)
        num_offsprings = self.pop_size[0] - num_parents

        for i in range(self.num_generations):
            fitness, team_budget = self.calc_fitness(self.population)
            fitness_history.append(fitness)
            team_budget_history.append(team_budget)

            parents = self.selection()
            offsprings = self.crossover()
            mutants = self.mutation()

            self.population[0 : parents.shape[0], :] = parents
            self.population[parents.shape[0] : , :] = mutants

        print('\nLast generation: \n{}\n'.format(self.population))
        fitness_last_gen = self.calc_fitness()
        print('\nFitness of the last generation: \n{}\n'.format(fitness_last_gen))
        max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
        parameters.append(self.population[max_fitness[0][0], :])

        return parameters, fitness_history

    def calc_fitness(self, population):
        # list of populations fitness
        fitness = []
        team_budget = []

        # for each solution
        for index, item in enumerate(population):
            fitness_individual, team_value_individual = self.population[index].get_individual_fitness(self.budget)
            fitness.append(fitness_individual)
            team_budget.append(team_value_individual)

        return fitness, team_budget

    def selection(self, fitness, num_parents, population):
        return None

    def crossover(self, parents, num_offsprings):
        return None

    def mutation(self, offsprings):
        return None

    # TODO CORRIGIR FUNCAO, ESTAVA APENAS PEGANDO OS PRIMEIROS ATLETAS, E NAO ALGO DE FATO RANDOMICO
    def get_initial_population(self):
        population = []

        # populate all solutions and return then
        for _ in range(self.solutions_per_pop):
            individual = Individual()
            individual.generate_solution()
            population.append(individual)

        return population

    def get_teams_by_player(self, player):
        player_team_id = player['clube_id']
        found_game = False

        for game in self.next_games:
            if game['clube_casa_id'] == player_team_id or game ['clube_visitante_id'] == player_team_id:
                home_team = game['clube_casa_id']
                visiting_team = game['clube_visitante_id']
                found_game = True

        return home_team, visiting_team if found_game else None