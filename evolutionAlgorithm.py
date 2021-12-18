from dataTypes import Chromosome, Gene, Codon
import random


class EvolutionAlgorithm:

    def __init__(self, network, population_size, random_seed):
        self.network = network
        self.population_size = population_size
        self.random_seed = random_seed
        pass

    def initialize_population(self):
        population = []

        for _ in range(self.population_size):
            population.append(self.initialize_chromosome())

        return population

    def initialize_chromosome(self):
        chromosome = Chromosome()
        for demand in self.network.demands:
            gene = Gene()
            codons_distribution = self.random_codon_distribution(len(demand.demand_paths), demand.demand_volume)

            for i, path in enumerate(demand.demand_paths):
                gene.codon.append(Codon(codons_distribution[i]))

            chromosome.genes.append(gene)
        return chromosome

    def random_codon_distribution(self, size, value):
        dist = [0] * size

        for _ in range(value):
            dist[random.randint(0, size - 1)] += 1

        return dist

    def run(self):
        random.seed(self.random_seed)
        population = self.initialize_population()
