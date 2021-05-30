import random

from constants import (BEST, BITS_FOR_VERTEX, MUTATE_GEN_PROBABILITY,
                       MUTATE_MEMBER_PROBABILITY, REPRODUCTION_POINT_DEVIDER,
                       REPRODUCTION_PROBABILITY, SHORTEST)


def reproduce_population(population, graph):
  reproduced_population = []
  for i in range(len(population) - 2):
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
    first_path_as_bits = graph.get_path_as_bits(first_path)
    second_path_as_bits = graph.get_path_as_bits(second_path)

    indexes = set()
    reproduced_path1 = [0] * len(first_path_as_bits)
    reproduced_path2 = [0] * len(second_path_as_bits)

    while True:
      indexes.add(random.randint(0, len(first_path_as_bits)))

      if len(indexes) >= int(len(first_path_as_bits) / REPRODUCTION_POINT_DEVIDER):
        break

    iteration = 0
    indexes = sorted(indexes)
    for i in range(len(first_path_as_bits) - 1):
      if i < indexes[iteration] or iteration == len(indexes) - 1:
        try:
          if iteration % 2 == 0:
            reproduced_path1[i] = first_path_as_bits[i]
            reproduced_path2[i] = second_path_as_bits[i]

          else:
            reproduced_path1[i] = second_path_as_bits[i]
            reproduced_path2[i] = first_path_as_bits[i]
        except:
          print("Error in reproduction: path1: {}, path2: {}, index: {}".format(first_path_as_bits, second_path_as_bits, i))
          raise
      else:
        iteration += 1
        i -= 1

    return graph.get_path_as_numbers(reproduced_path1), graph.get_path_as_numbers(reproduced_path2)

  else:
    return first_path, second_path


def mutate(reproduced_members, graph):
  for i in range(len(reproduced_members) - 1):
    if random.randint(0, 100) <= MUTATE_MEMBER_PROBABILITY:
      reproduced_members[i][SHORTEST] = mutate_path(
          reproduced_members[i][SHORTEST], graph)
      reproduced_members[i][BEST] = mutate_path(reproduced_members[i][BEST], graph)
  return reproduced_members


def mutate_path(path, graph):
  path_as_bits = graph.get_path_as_bits(path)
  new_path = []
  for i in range(0, len(path_as_bits) - 1, BITS_FOR_VERTEX):
    if random.randint(0, 100) <= MUTATE_GEN_PROBABILITY:
      for j in range(BITS_FOR_VERTEX - 1):
        new_path.append(random.randint(0, 1))
    else:
      for j in range(BITS_FOR_VERTEX - 1):
        new_path.append(path_as_bits[i + j])

  return graph.get_path_as_numbers(new_path)
