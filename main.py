from parser import *
from evolutionAlgorithm import *

POPULATION = 10
RANDOM_SEED = 913
MODE = Modes.DAP
STOP = StopCriteria(Criterion.TimeInSeconds, 3)


def run():
    network_name = 'data/net4.txt'
    network = Parser().openFile(network_name)
    e = EvolutionAlgorithm(network, POPULATION, RANDOM_SEED, MODE, STOP)
    e.run()
    pass


if __name__ == '__main__':
    run()
