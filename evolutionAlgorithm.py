from datetime import datetime as dt
from typing import List
from dataTypes import Chromosome, Gene, Codon, StopCriteria, Criterion, Modes
import random
import copy


class EvolutionAlgorithm:

    def __init__(self, network, population_size, random_seed, mode: Modes, stop_criteria: StopCriteria):
        self.network = network
        self.population_size = population_size
        self.random_seed = random_seed
        self.mode = mode
        self.cost_function = self.set_up_cost_function()
        self.stop_criteria = stop_criteria

    def set_up_cost_function(self):
        if self.mode == Modes.DAP:
            return self.dap_cost_function
        else:
            return self.ddap_cost_function

    def dap_cost_function(self, chromosome: Chromosome):
        demand_units = [0] * len(self.network.links)
        for gene in chromosome.genes:
            for codon in gene.codons:
                for link in codon.path.link_list:
                    demand_units[link - 1] += codon.value

        link_overload_modules = [0] * len(self.network.links)
        for i, link in enumerate(self.network.links):
            link_overload_modules[i] = demand_units[i] - (link.number_of_modules * link.link_module)

        chromosome.cost = max(link_overload_modules)

    def ddap_cost_function(self, chromosome: Chromosome):
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
                gene.codons.append(Codon(codons_distribution[i], path))

            chromosome.genes.append(gene)

        self.cost_function(chromosome)
        return chromosome

    def random_codon_distribution(self, size, value):
        dist = [0] * size

        for _ in range(value):
            dist[random.randint(0, size - 1)] += 1

        return dist

    def cost_function(self, chromosome):
        pass

    def should_stop(self):
        if self.stop_criteria.criterion == Criterion.TimeInSeconds:
            if self.stop_criteria.seconds_passed > self.stop_criteria.threshold_value:
                return True
        elif self.stop_criteria.criterion == Criterion.Generations:
            if self.stop_criteria.generations_passed > self.stop_criteria.threshold_value:
                return True
        elif self.stop_criteria.criterion == Criterion.Mutations:
            if self.stop_criteria.mutations_passed > self.stop_criteria.threshold_value:
                return True
        elif self.stop_criteria.criterion == Criterion.NoImprovementInGenerations:
            if self.stop_criteria.no_improvements_passed > self.stop_criteria.threshold_value:
                return True

        return False

    def create_new_population(self, population):
        pass

    def mutate_population(self, population):
        pass

    def dispose_population(self, population):
        pass

    def get_fittest_chromosome(self, population):
        fittest_chromosome: Chromosome = population[0]
        for chromosome in population:
            if chromosome.cost < fittest_chromosome.cost:
                fittest_chromosome = chromosome

        return fittest_chromosome

    def append_fittest_chromosome(self, population, fittest_chromosomes):
        fittest_chromosome = self.get_fittest_chromosome(population)
        min_cost = fittest_chromosomes[0]

        for chromosome in fittest_chromosomes:
            if chromosome.cost < min_cost:
                min_cost = chromosome.cost

        if fittest_chromosome.cost < min_cost:
            fittest_chromosomes.append(copy.deepcopy(fittest_chromosome))
            self.stop_criteria.no_improvements_passed = 0
        else:
            self.stop_criteria.no_improvements_passed += 1

    def update_generation_metadata(self, start_time):
        self.stop_criteria.seconds_passed = (dt.now() - start_time).total_seconds()
        self.stop_criteria.generations_passed += 1
        # TODO: Mutation passed criterion

    def run(self):
        fittest_chromosomes: List[Chromosome] = []
        start_time = dt.now()
        random.seed(self.random_seed)
        population = self.initialize_population()
        fittest_chromosomes.append(copy.deepcopy(self.get_fittest_chromosome(population)))

        while not self.should_stop():

            self.create_new_population(population)
            self.mutate_population(population)
            self.dispose_population(population)

            self.update_generation_metadata(start_time)

