import numpy as np
import random
import copy

class GeneticAlgorithm:

    def __init__(self, dna_length, fitness_function, max_pop, max_gen, mutation_rate=0.05, mutation_severity=1):
        self.dna_length = dna_length
        self.fitness_function = fitness_function
        self.max_pop = max_pop
        self.max_gen = max_gen
        self.mutation_rate = mutation_rate
        self.mutation_severity = mutation_severity

    class Individual:
        def __init__(self, array, fitness_function):
            self.array = array
            self.fitness_function = fitness_function
            self.fitness = 0
            self.num_times_estimated = 0

        def get_fitness(self):
            this_estimate = self.fitness_function(self.array)
            self.fitness = (self.fitness * self.num_times_estimated + this_estimate) / (self.num_times_estimated + 1)
            self.num_times_estimated += 1

    def evolve(self):
        # Initialize population
        population = self.population_initialization()
        half_pop = int(self.max_pop / 2)
        # Start evolution
        for generation in range(self.max_gen):
            for individual in population:
                individual.get_fitness()
            population.sort(key=lambda x: -x.fitness)
            for i in range(half_pop, len(population)):
                mother = random.choice(population[:half_pop])
                father = random.choice(population[:half_pop])
                population[i] = self.Individual(self.recombine(mother, father), self.fitness_function)
                self.mutate(population[i])
            # logging
            print(f'Generation: {generation}, '
                  f'best fitness: {format(population[0].fitness, ".0f")}, '
                  f'age: {format(population[0].num_times_estimated, ".0f")}, '
                  f'middle fitness: {format(population[half_pop - 1].fitness, ".0f")}, '
                  f'best genome: {[format(e, ".2f") for e in population[0].array]}')
            #print(population[0].fitness, population[half_pop - 1].fitness, population[0].array)
        return population[0].array

    def population_initialization(self):
        population = []
        for i in range(self.max_pop):
            population.append(self.Individual(np.random.rand(self.dna_length) * 2 - 1, self.fitness_function))
        return population

    def recombine(self, mother, father):
        new_genome = copy.copy(father.array)
        indices_from_mother = np.random.choice(self.dna_length, int(self.dna_length / 2), replace=False)
        new_genome[indices_from_mother] = mother.array[indices_from_mother]
        return new_genome

    def mutate(self, individual):
        num_mutations = np.random.binomial(self.dna_length, self.mutation_rate)
        mutation_indices = np.random.choice(self.dna_length, num_mutations, replace=False)
        mutation_delta = np.random.rand(num_mutations) * 2 * self.mutation_severity - self.mutation_severity
        individual.array[mutation_indices] += mutation_delta


if __name__ == '__main__':
    def trial_fitness_func(array):
        return - abs(5 - sum(array)) + 10

    ga = GeneticAlgorithm(10, trial_fitness_func, 10, 10, mutation_rate=0.5)
    print(ga.evolve())
