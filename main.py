import sys

from Chromosome import Chromosome
from PCBData import PCBData
from GA import roulette
from GA import tournament
from GA import crossover
from GA import genetic_algorithm

if __name__ == '__main__':

    population = []

    pcb_data = PCBData("zad1.txt")
    pcb_data.read_file()


    # print(pcb_data.pcb_height)
    # print(pcb_data.pcb_width)
    # print(pcb_data.pcb_path_points)

    # chromosome = Chromosome(pcb_data)
    # chromosome.generate_random_paths()

    # chromosome.print_me()
    # print(f"Penalty points: {chromosome.penalty_function()}")

    # best = sys.maxsize

    for i in range(1000):
        chromosome = Chromosome(pcb_data)
        chromosome.generate_random_paths()
        population.append(chromosome)
    print('Population generated!')

    genetic_algorithm(population, 10)



    # chromosome1 = Chromosome(pcb_data)
    # chromosome1.generate_random_paths()
    #
    # chromosome2 = Chromosome(pcb_data)
    # chromosome2.generate_random_paths()
    #
    # print(f" punkty pierwszego: {chromosome1.penalty_function()}")
    # print(f" punkty drugiego: {chromosome2.penalty_function()}")
    #
    # child = crossover(chromosome1, chromosome2)
    #
    # print(f" punkty dziecka: {child.penalty_function()}")

    # from_roulette1 = roulette(population, 10)
    # best1 = tournament(from_roulette1)
    #
    # from_roulette2 = roulette(population, 10)
    # best2 = tournament(from_roulette)