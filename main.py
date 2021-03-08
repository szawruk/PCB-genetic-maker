import sys

from Chromosome import Chromosome
from PCBData import PCBData

if __name__ == '__main__':
    pcb_data = PCBData("zad1.txt")
    pcb_data.read_file()

    # print(pcb_data.pcb_height)
    # print(pcb_data.pcb_width)
    # print(pcb_data.pcb_path_points)

    # chromosome = Chromosome(pcb_data)
    # chromosome.generate_random_paths()
    # chromosome.print_me()
    # print(f"Penalty points: {chromosome.penalty_function()}")

    best = sys.maxsize
    for i in range(100):
        chromosome = Chromosome(pcb_data)
        chromosome.generate_random_paths()

        points = chromosome.penalty_function()
        if points < best:
            best = min(best, points)
            chromosome.print_me()

    print(f"Best penalty points: {best}")
