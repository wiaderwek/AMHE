import random

from constants import (BEST, BITS_FOR_VERTEX, MUTATE_GEN_PROBABILITY,
                       MUTATE_MEMBER_PROBABILITY, REPRODUCTION_POINT_DIVIDER,
                       REPRODUCTION_PROBABILITY, SHORTEST)


def reproduce_population(population, graph):
  reproduced_population = []
  for i in range(len(population) - 1):
    rep_mem1, rep_mem2 = reproduce_members(population[i][0], population[i + 1][0], graph)
    reproduced_population.append(rep_mem1)
    reproduced_population.append(rep_mem2)

  return reproduced_population

def reproduce_members(first_member, second_member, graph):
  first_shortes, second_shortest = reproduce_path(first_member[SHORTEST],
                                                  second_member[SHORTEST], graph)
  first_best, second_best = reproduce_path(first_member[BEST],
                                           second_member[BEST], graph)

  return {
      SHORTEST: first_shortes,
      BEST: first_best
  }, {
      SHORTEST: second_shortest,
      BEST: second_best
  }


def reproduce_path(first_path, second_path, graph):
  if random.randint(0, 100) <= REPRODUCTION_PROBABILITY:

    indexes = set()
    reproduced_path1 = [graph.get_random_vertex() for _ in range(len(first_path))]
    reproduced_path2 = [graph.get_random_vertex() for _ in range(len(first_path))]

    while True:
      indexes.add(random.randint(0, len(first_path) - 1))

      if len(indexes) >= int(len(first_path) / REPRODUCTION_POINT_DIVIDER):
        break

    iteration = 0
    indexes = sorted(indexes)
    for i in range(len(first_path)):
      if iteration < len(indexes) and i >= indexes[iteration]:
        iteration += 1

      if iteration % 2 == 0:
        reproduced_path1[i] = first_path[i]
        reproduced_path2[i] = second_path[i]

      else:
        reproduced_path1[i] = second_path[i]
        reproduced_path2[i] = first_path[i]

    return reproduced_path1, reproduced_path2

  else:
    return first_path, second_path


def mutate(reproduced_members, graph):
  for i in range(len(reproduced_members)):
    if random.randint(0, 100) <= MUTATE_MEMBER_PROBABILITY:
      reproduced_members[i][SHORTEST] = mutate_path(
          reproduced_members[i][SHORTEST], graph)
      reproduced_members[i][BEST] = mutate_path(reproduced_members[i][BEST], graph)
  return reproduced_members


def mutate_path(path, graph):
  new_path = []
  new_path.append(path[0])
  for i in range(1, len(path) - 1, 1):
    if random.randint(0, 100) <= MUTATE_GEN_PROBABILITY:
      new_path.append(graph.get_mutate_vertex(path[i]))
    else:
      new_path.append(path[i])
  new_path.append(path[len(path) - 1])

  return new_path
