import numpy as np
from random import randrange


from individual import Individual

# TODO MELHORAR FUNC FITNESS


# TODO CROSSOVER
# fazer funcao em individual, que ordena a lista de index dos jogadores q tao no time,
# dai o slection do cartola corta no meio e troca e ve o fitness novamente


# Has the responsability to manage individuals
class Cartola:
    population: list[Individual]
    budget: int
    num_generations: int
    solutions_per_pop: int

    def __init__(self, budget, num_generations=150, solutions_per_pop=8):
        self.budget = budget
        self.num_generations = num_generations
        self.solutions_per_pop = solutions_per_pop
        self.population = self.get_initial_population()

    def optimize(self):
        parameters, fitness_history, team_budget_history = [], [], []
        num_offsprings = self.solutions_per_pop - 2

        for _ in range(self.num_generations):
            fitness, team_budget = self.calc_fitness(self.population)
            fitness_history.append(fitness)
            team_budget_history.append(team_budget)

            parents = self.selection(self.population)
            offsprings = self.crossover(parents, num_offsprings)
            mutants = self.mutation()

        print('\nLast generation: \n{}\n'.format(self.population))
        fitness_last_gen = self.calc_fitness()
        print('\nFitness of the last generation: \n{}\n'.format(fitness_last_gen))
        max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
        parameters.append(self.population[max_fitness[0][0], :])

        return parameters, fitness_history

    def calc_fitness(self, population: list[Individual]):
        # list of populations fitness
        fitness = []
        team_budget = []

        # for each solution
        for index, item in enumerate(population):
            fitness_individual, team_value_individual = self.population[index].get_individual_fitness(
                self.budget)

            fitness.append(fitness_individual)
            team_budget.append(team_value_individual)

        return fitness, team_budget

    def selection(self, population: list[Individual]) -> list[Individual]:
        parent_1 = population[0]
        parent_2 = population[-1]

        fitness_values = [individual.get_team_fitness()
                          for individual in population]
        fitness_values.sort(reverse=True)
        fitness_values = fitness_values[:2]

        for item in population:
            if item.get_team_fitness() == fitness_values[0]:
                parent_1 = item
            elif item.get_team_fitness() == fitness_values[1]:
                parent_2 = item

        return [parent_1, parent_2]

    # TODO HERE

    def crossover(self, parents: list[Individual], num_offsprings: int):
        parent_1 = dict()
        parent_2 = dict()
        children: list[Individual]

        for idx, i in enumerate(parents[0].get_individual_population()):
            if i == 1:
                parent_1[idx] = parents[0].get_player(idx).posicao_id

        for idx, i in enumerate(parents[1].get_individual_population()):
            if i == 1:
                parent_2[idx] = parents[1].get_player(idx).posicao_id

        #

        for idx in range(num_offsprings):
            max_changes = randrange(6)
            changes = 0

            while changes <= max_changes:
                for idx_i, i in enumerate(parent_1):
                    for idx_j, j in enumerate(parent_2):
                        if parent_1[idx_i] == parent_2[idx_j]:
                            aux = parent_2[idx_j]
                            parent_2[idx_j] = parent_1[idx_i]
                            parent_1[idx_i] = aux

                            changes += 1

        print("")

        return None

    def mutation(self, offsprings):
        return None

    # TODO CORRIGIR FUNCAO, ESTAVA APENAS PEGANDO OS PRIMEIROS ATLETAS, E NAO ALGO DE FATO RANDOMICO
    def get_initial_population(self) -> list[Individual]:
        population: list[Individual] = []

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
            if game['clube_casa_id'] == player_team_id or game['clube_visitante_id'] == player_team_id:
                home_team = game['clube_casa_id']
                visiting_team = game['clube_visitante_id']
                found_game = True

        return home_team, visiting_team if found_game else None
