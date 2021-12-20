from parser import *
from evolutionAlgorithm import *
from cmd import *

POPULATION = 500
RANDOM_SEED = 23452344
MODE = Modes.DAP
STOP = StopCriteria(Criterion.Generations, 500)
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.05
network_name = InputFiles.net4
network_file = 'data/' + network_name.name + '.txt'

RUN_CMD = True


def run():
    if RUN_CMD:
        population, random_seed, mode, stop, stop_value, crossover_p, mutation_p, net = get_parameters()
        network = Parser().openFile('data/' + net.name + '.txt')
        e = EvolutionAlgorithm(network, population, random_seed, mode, StopCriteria(stop, stop_value), crossover_p, mutation_p, net)
    else:
        network = Parser().openFile(network_file)
        e = EvolutionAlgorithm(network, POPULATION, RANDOM_SEED,
                               MODE, STOP, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, network_name)

    e.run()


if __name__ == '__main__':
    run()
