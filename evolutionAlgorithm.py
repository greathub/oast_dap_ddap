from datetime import datetime as dt
from dataTypes import Chromosome, Gene, Codon, StopCriteria, Criterion, Modes, FittestChromosome
import random
import copy
from math import ceil


class EvolutionAlgorithm:

    def __init__(self, network, population_size, random_seed,
                 mode: Modes, stop_criteria: StopCriteria, crossover_probability,
                 mutation_probability, network_name):
        self.network = network
        self.population_size = population_size
        self.random_seed = random_seed
        self.mode = mode
        self.cost_function = self.set_up_cost_function()
        self.stop_criteria = stop_criteria
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.network_name = network_name

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
        link_demands, link_cost = [0] * len(self.network.links), [0] * len(self.network.links)
        for gene in chromosome.genes:
            for codon in gene.codons:
                for link in codon.path.link_list:
                    link_demands[link - 1] += codon.value

        for i, link in enumerate(self.network.links):
            link_cost[i] = ceil(link_demands[i] / link.link_module) * link.module_cost
        chromosome.cost = sum(link_cost)

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

    def normalize_fitness_function(self, population):
        costs = [chromosome.cost for chromosome in population]
        min_cost, max_cost = min(costs), max(costs)

        if min_cost == max_cost:
            fitness_function_sum = len(population)
        else:
            fitness_function_sum = 0

        for chromosome in population:
            if min_cost == max_cost:
                chromosome.fitness_function = 1
            else:
                chromosome.fitness_function = (max_cost - chromosome.cost) / (max_cost - min_cost)
                fitness_function_sum += chromosome.fitness_function

        return fitness_function_sum

    def create_next_generation(self, population):
        fitness_function_sum = self.normalize_fitness_function(population)

        chromosomes_to_cross = []

        const_prob = self.crossover_probability * len(population) / fitness_function_sum
        for chromosome in population:
            if random.random() < const_prob * chromosome.fitness_function:
                chromosomes_to_cross.append(chromosome)

        chromosomes_to_cross = copy.deepcopy(chromosomes_to_cross)
        # Parents selection randomly:
        # num = int(len(chromosomes_to_cross)/2)
        # for i in range(num):
        #     first = random.randint(0, len(chromosomes_to_cross) - 1)
        #     first_chromosome = chromosomes_to_cross.pop(first)
        #     second = random.randint(0, len(chromosomes_to_cross) - 1)
        #     second_chromosome = chromosomes_to_cross.pop(second)
        #     first_child, second_child = self.crossover(first_chromosome, second_chromosome)
        #     population.append(first_child)
        #     population.append(second_child)
        # Parents selection queen of the bees:
        queen = self.get_fittest_chromosome(population)
        for chromosome in chromosomes_to_cross:
            first_child, second_child = self.crossover(chromosome, queen)
            population.append(first_child)
            population.append(second_child)

    def crossover(self, chromosome_a: Chromosome, chromosome_b: Chromosome):
        first_child, second_child = Chromosome(), Chromosome()

        for gene_a, gene_b in zip(chromosome_a.genes, chromosome_b.genes):
            if random.random() < 0.5:
                first_child.genes.append(gene_a)
                second_child.genes.append(gene_b)
            else:
                first_child.genes.append(gene_b)
                second_child.genes.append(gene_a)

        self.cost_function(first_child)
        self.cost_function(second_child)

        return first_child, second_child

    def mutate_population(self, population):

        for chromosome in population:
            for gene in chromosome.genes:
                if random.random() < self.mutation_probability:
                    self.mutate_gene(gene)

    def mutate_gene(self, gene):
        if len(gene.codons) < 2:
            return

        first, second = random.randint(0, len(gene.codons) - 1), random.randint(0, len(gene.codons) - 1)

        while gene.codons[first].value < 1 or first == second:
            first, second = random.randint(0, len(gene.codons) - 1), random.randint(0, len(gene.codons) - 1)

        gene.codons[first].value -= 1
        gene.codons[second].value += 1
        self.stop_criteria.mutations_passed += 1

    def dispose_population(self, population):
        population.sort(key=lambda x: x.cost)
        del population[self.population_size:]

    def get_fittest_chromosome(self, population):
        fittest_chromosome: Chromosome = population[0]
        for chromosome in population:
            if chromosome.cost < fittest_chromosome.cost:
                fittest_chromosome = chromosome

        return fittest_chromosome

    def append_fittest_chromosome(self, population, fittest_chromosomes):
        fittest_chromosome = self.get_fittest_chromosome(population)
        min_cost = fittest_chromosomes.chromosomes[0].cost

        for chromosome in fittest_chromosomes.chromosomes:
            if chromosome.cost < min_cost:
                min_cost = chromosome.cost

        if fittest_chromosome.cost < min_cost:
            fittest_chromosomes.append(copy.deepcopy(fittest_chromosome), self.stop_criteria.generations_passed)
            self.stop_criteria.no_improvements_passed = 0
        else:
            self.stop_criteria.no_improvements_passed += 1

    def update_generation_metadata(self, start_time):
        self.stop_criteria.seconds_passed = (dt.now() - start_time).total_seconds()
        self.stop_criteria.generations_passed += 1

    def log_information(self, population):
        basic = self.stop_criteria
        smallest_cost = self.get_fittest_chromosome(population).cost
        info = "Generation: {}, smallest cost: {}, time {}". \
            format(basic.generations_passed, smallest_cost, basic.seconds_passed)
        print(info)

    def run(self):
        fittest_chromosomes = FittestChromosome()
        start_time = dt.now()
        random.seed(self.random_seed)
        population = self.initialize_population()
        fittest_chromosomes.append(copy.deepcopy(self.get_fittest_chromosome(population)), 0)

        while not self.should_stop():
            self.create_next_generation(population)
            self.mutate_population(population)
            self.dispose_population(population)

            self.update_generation_metadata(start_time)

            self.append_fittest_chromosome(population, fittest_chromosomes)
            self.log_information(fittest_chromosomes.chromosomes)

        for (chromosome, generation) in zip(fittest_chromosomes.chromosomes, fittest_chromosomes.generations):
            self.save_chromosome_to_file(chromosome, generation)

    def save_chromosome_to_file(self, chromosome: Chromosome, generation):
        log = "Generation: {}\nCost: {}\nSeconds passed: {}"\
            .format(generation, chromosome.cost, self.stop_criteria.seconds_passed)
        link_number = len(self.network.links)
        log += "{}\n\n".format(link_number)
        demands_of_links, modules_of_links = [0] * link_number, [0] * link_number
        for gene in chromosome.genes:
            for codon in gene.codons:
                for link in codon.path.link_list:
                    demands_of_links[link - 1] += codon.value
        for i, link in enumerate(self.network.links):
            modules_of_links[i] = -(-demands_of_links[i]//link.link_module)

        for i in range(link_number):
            log += "{} {} {}\n".format(i + 1, demands_of_links[i], modules_of_links[i])

        log += '\n\n' + str(len(chromosome.genes)) + '\n'

        for i, gene in enumerate(chromosome.genes):
            log += "\n{} {}".format(i+1, len(gene.codons))
            for j, codon in enumerate(gene.codons):
                log += "\n{} {}".format(j+1, codon.value)
            log += "\n"

        file_name = 'output/' + str(self.network_name.name) + str(self.mode.value) + '.txt'

        with open(file_name, "a") as file:
            file.write(log)
