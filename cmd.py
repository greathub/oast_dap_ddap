from dataTypes import Modes, Criterion, InputFiles


def get_parameters():
    net, population, random_seed, stop, stop_value, crossover_p, mutation_p = 0, 0, 0, 0, 0, 0, 0
    mode = ""

    while net not in [1, 2, 3]:
        try:
            print("Podaj, numer odpowiadający plikowi: ")
            [print("{} dla {}".format(i+1, c.name)) for i, c in enumerate(InputFiles)]
            net = int(input())
        except ValueError:
            continue
    net = InputFiles(net)

    while not population:
        try:
            population = int(input("Podaj liczność populacji: "))
        except ValueError:
            continue

    while not random_seed:
        try:
            random_seed = int(input("Podaj ziarno generatora: "))
        except ValueError:
            continue

    while mode not in ["DAP", "DDAP"]:
        try:
            mode = input("Podaj typ rozwiązania (DAP, DDAP): ")
        except ValueError:
            continue
    mode = Modes[mode]

    while stop not in [1, 2, 3, 4]:
        try:
            print("Podaj liczbę odpowiadającą kryterium stopu:")
            [print("{} dla {}".format(c.value + 1, c.name)) for c in Criterion]
            stop = int(input())
        except ValueError:
            continue
    stop = Criterion(stop - 1)

    while not stop_value:
        try:
            stop_value = int(input("Podaj wartość graniczną dla kryterium stopu: "))
        except ValueError:
            continue

    while crossover_p >= 1 or crossover_p <= 0:
        try:
            crossover_p = float(input("Podaj prawdopodobieństwo krzyżowania: "))
        except ValueError:
            continue

    while mutation_p >= 1 or mutation_p <= 0:
        try:
            mutation_p = float(input("Podaj prawdopodobieństwo mutowania: "))
        except ValueError:
            continue

    return population, random_seed, mode, stop, stop_value,   crossover_p, mutation_p, net
