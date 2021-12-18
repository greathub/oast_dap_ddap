import enum


class Link:
    def __init__(self, link_array):
        self.start_node = int(link_array[0])
        self.end_node = int(link_array[1])
        self.number_of_modules = int(link_array[2])
        self.module_cost = int(link_array[3])
        self.link_module = int(link_array[4])


class Demand:
    def __init__(self, demand_array, demand_id):
        self.demand_id = demand_id
        self.start_node = int(demand_array[0])
        self.end_node = int(demand_array[1])
        self.demand_volume = int(demand_array[2])
        self.demand_paths = []


class DemandPath:
    def __init__(self, demand_path_array):
        self.demand_path_id = int(demand_path_array[0])
        self.link_list = [int(d) for d in demand_path_array[1:]]


class Network:
    def __init__(self):
        self.links = []
        self.demands = []


class Codon:
    def __init__(self, value, path):
        self.value = value
        self.path = path


class Gene:
    def __init__(self):
        self.codons = []


class Chromosome:
    def __init__(self):
        self.genes = []
        self.cost = float('inf')  # https://stackoverflow.com/a/34264749
        self.fitness_function = 0


class StopCriteria:
    def __init__(self, criterion, threshold_value):
        self.criterion: Criterion = criterion
        self.threshold_value = threshold_value
        self.seconds_passed = 0
        self.generations_passed = 0
        self.mutations_passed = 0
        self.no_improvements_passed = 0


class Criterion(enum.Enum):
    TimeInSeconds = 0
    Generations = 1
    Mutations = 2
    NoImprovementInGenerations = 3


class Modes(enum.Enum):
    DAP = 0
    DDAP = 1
