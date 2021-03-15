import random
from copy import deepcopy
from typing import List

import numpy

from Chromosome import Chromosome
from Segment import Segment

CROSSOVER_P1 = 0.8
CROSSOVER_P = 0.5
CROSSOVER_CHILDREN_NUMBER = 3
MUTATION_PATH_CHANGE_P = 0.2
MUTATION_SEGMENT_CHANGE_P = 0.1


def roulette(pop, percent):
    total_points = 0
    roulette_point_widths = []
    res_population = []

    for specimen in pop:
        total_points += specimen.penalty_function()

    for specimen in pop:
        roulette_point_widths.append(specimen.penalty_function() / total_points)

    roulette_point_widths = sorted(roulette_point_widths, reverse=True)

    pop_sorted = sorted(pop, key=lambda chromosome: chromosome.penalty_function())

    specimens_added = 0
    while specimens_added < percent * len(pop):
        draw_point = random.random()
        total = 0
        for idx, roulette_point_width in enumerate(roulette_point_widths):
            total += roulette_point_width
            if total >= draw_point and pop_sorted not in res_population:
                res_population.append(pop_sorted[idx])
                specimens_added += 1
                break

    return res_population


def tournament(pop: List[Chromosome]):
    return min(pop, key=lambda specimen: specimen.penalty_function())


def crossover(parent1: Chromosome, parent2: Chromosome):
    children = []
    for i in range(CROSSOVER_CHILDREN_NUMBER):
        child = Chromosome(parent1.pcb_data_object)
        for path_number in range(len(parent1.paths)):
            if random.random() > CROSSOVER_P:
                child.paths.append(deepcopy(parent1.paths[path_number]))
            else:
                child.paths.append(deepcopy(parent2.paths[path_number]))
        children.append(child)

    return tournament(children)


def mutation(chromosome: Chromosome):
    for path in chromosome.paths:
        if random.random() < MUTATION_PATH_CHANGE_P:
            segment_idx = 0
            while segment_idx < len(path.segments):
                if random.random() < MUTATION_SEGMENT_CHANGE_P:
                    direction = random.choice([-1, 1])
                    if abs(path.segments[segment_idx].direction) == 1:  # segment jest pionowo, wiec przesuwamy poziomo
                        direction *= 2

                    # jest tylko jeden segment
                    if len(path.segments) == 1:
                        path.segments.insert(0, Segment(direction, 1))
                        path.segments.insert(2, Segment(direction * (-1), 1))
                        segment_idx += 2

                    # dany segment nie jest pierwszy ani końcowy
                    elif segment_idx != 0 and segment_idx < len(path.segments) - 1:
                        # oba okalające segmenty są w jednej linii z aktualnie mutowanym segmentem
                        if path.segments[segment_idx - 1].direction == path.segments[segment_idx].direction and path.segments[segment_idx + 1].direction == path.segments[segment_idx].direction:
                            path.segments.insert(segment_idx, Segment(direction, 1))
                            path.segments.insert(segment_idx + 2, Segment(direction * (-1), 1))
                            segment_idx += 3
                        # tylko poprzedni segment jest w jednej linii z aktualnie mutowanym segmentem
                        elif path.segments[segment_idx - 1].direction == path.segments[segment_idx].direction:
                            path.segments.insert(segment_idx, Segment(direction, 1))
                            path.segments[segment_idx + 2].length -= numpy.sign(direction) * numpy.sign(path.segments[segment_idx + 2].direction)
                            if path.segments[segment_idx + 2].length == 0:
                                path.segments.pop(segment_idx + 2)
                            segment_idx += 2
                        # tylko następny segment jest w jednej linii z aktualnie mutowanym segmentem
                        elif path.segments[segment_idx + 1].direction == path.segments[segment_idx].direction:
                            path.segments.insert(segment_idx + 1, Segment(direction * (-1), 1))
                            path.segments[segment_idx - 1].length += numpy.sign(direction) * numpy.sign(path.segments[segment_idx + 2].direction)
                            if path.segments[segment_idx - 1].length == 0:
                                path.segments.pop(segment_idx - 1)
                                segment_idx += 1
                            else:
                                segment_idx += 2
                        # segmenty okalające nie są w jednej linii z sąsiadami
                        else:
                            path.segments[segment_idx - 1].length += numpy.sign(direction) * numpy.sign(path.segments[segment_idx - 1].direction)
                            path.segments[segment_idx + 1].length -= numpy.sign(direction) * numpy.sign(path.segments[segment_idx + 1].direction)

                            if path.segments[segment_idx - 1].length == 0 and path.segments[segment_idx + 1].length == 0:
                                path.segments.pop(segment_idx - 1)
                                path.segments.pop(segment_idx)

                            elif path.segments[segment_idx - 1].length == 0:
                                path.segments.pop(segment_idx - 1)

                            elif path.segments[segment_idx + 1].length == 0:
                                path.segments.pop(segment_idx + 1)
                                segment_idx += 1
                            else:
                                segment_idx += 1

                    # jeżeli segment jest pierwszy
                    elif segment_idx == 0:
                        # jeżeli następny segment jest w tym samym kierunku
                        if path.segments[segment_idx + 1].direction == path.segments[segment_idx].direction:
                            path.segments.insert(segment_idx, Segment(direction, 1))
                            path.segments.insert(segment_idx + 2, Segment(direction * (-1), 1))
                            segment_idx += 3
                        # następny segment jest prostopadły
                        else:
                            path.segments.insert(segment_idx, Segment(direction, 1))
                            path.segments[segment_idx + 1].length -= numpy.sign(direction) * numpy.sign(path.segments[segment_idx + 1].direction)
                            if path.segments[segment_idx + 1].length == 0:
                                path.segments.pop(segment_idx + 1)
                            segment_idx += 2

                    # jeżeli segment jest ostatni
                    elif segment_idx == len(path.segments) - 1:
                        # jeżeli poprzedni segment jest w tym samym kierunku
                        if path.segments[segment_idx - 1].direction == path.segments[segment_idx].direction:
                            path.segments.insert(segment_idx, Segment(direction, 1))
                            path.segments.insert(segment_idx + 2, Segment(direction * (-1), 1))
                            segment_idx += 3
                        # poprzedni segment jest prostopadły
                        else:
                            path.segments.insert(segment_idx + 1, Segment(direction, 1))
                            path.segments[segment_idx - 1].length += numpy.sign(direction) * numpy.sign(path.segments[segment_idx - 1].direction)
                            if path.segments[segment_idx - 1].length == 0:
                                path.segments.pop(segment_idx - 1)
                        segment_idx += 2

    chromosome.penalty_function(refresh=True)
    return chromosome


def genetic_algorithm(population: List[Chromosome], epochs: int):
    start_population = population
    best_solution = None

    for epoch in range(epochs):
        new_population = []
        best_solution_in_epoch = None
        worst_solution_in_epoch_penalty_points = None
        worst_solution_in_epoch_index = None

        while len(start_population) != len(new_population):
            specimen1 = tournament(roulette(population, 0.1))
            specimen2 = tournament(roulette(population, 0.1))
            if random.random() < CROSSOVER_P1:
                new_specimen = crossover(specimen1, specimen2)
            else:
                new_specimen = deepcopy(tournament([specimen1, specimen2]))
            new_specimen = mutation(new_specimen)
            new_population.append(new_specimen)

            if best_solution is None or best_solution.penalty_function() > new_specimen.penalty_function():
                best_solution = new_specimen

            if best_solution_in_epoch is None or best_solution_in_epoch.penalty_function() > new_specimen.penalty_function():
                best_solution_in_epoch = new_specimen

            if worst_solution_in_epoch_penalty_points is None or worst_solution_in_epoch_penalty_points < new_specimen.penalty_function():
                worst_solution_in_epoch_penalty_points = new_specimen.penalty_function()
                worst_solution_in_epoch_index = len(new_population) - 1

        if best_solution.penalty_function() < best_solution_in_epoch.penalty_function():
            population.pop(worst_solution_in_epoch_index)
            population.append(deepcopy(best_solution))
            print("Dodano najlepszego osobnika z poprzedniej populacji!")

        print(f"epoch {epoch + 1} ###### BEST =>>> {best_solution.penalty_function()}")
        start_population = new_population
    return best_solution
