import random

from constants import (BEST, BITS_FOR_VERTEX, MUTATE_GEN_PROBABILITY,
                       MUTATE_MEMBER_PROBABILITY, REPRODUCTION_POINT_DEVIDER,
                       REPRODUCTION_PROBABILITY, SHORTEST)


def reproduce_members(first_member, second_member):
  first_shortes, second_shortest = reproduce_path(first_member[SHORTEST],
                                                  second_member[SHORTEST])
  first_best, second_best = reproduce_path(first_member[BEST],
                                           second_member[BEST])

  return {
      SHORTEST: first_shortes,
      BEST: first_best
  }, {
      SHORTEST: second_shortest,
      BEST: second_best
  }


def reproduce_path(first_path, second_path):
  if random.randint(0, 100) <= REPRODUCTION_PROBABILITY:
    indexes = set()
    reproduced_path1 = []
    reproduced_path2 = []

    while True:
      indexes.add(random.randint(0, len(first_path)))

      if len(indexes) >= int(len(first_path) / REPRODUCTION_POINT_DEVIDER):
        break

    iteration = 0
    indexes = sorted(indexes)
    for i in range(len(first_path) - 1):
      if i < indexes[iteration] or iteration == len(indexes) - 1:
        if iteration % 2 == 0:
          reproduced_path1.append(first_path[i])
          reproduced_path2.append(second_path[i])

        else:
          reproduced_path1.append(second_path[i])
          reproduced_path2.append(first_path[i])
      else:
        iteration += 1
        i -= 1

    return reproduced_path1, reproduced_path2

  else:
    return first_path, second_path


def mutate(reproduced_members):
  for i in range(len(reproduced_members) - 1):
    if random.randint(0, 100) <= MUTATE_MEMBER_PROBABILITY:
      reproduced_members[i][SHORTEST] = mutate_path(
          reproduced_members[i][SHORTEST])
      reproduced_members[i][BEST] = mutate_path(reproduced_members[i][BEST])
  return reproduced_members


def mutate_path(path):
  new_path = []
  for i in range(0, len(path) - 1, BITS_FOR_VERTEX):
    if random.randint(0, 100) <= MUTATE_GEN_PROBABILITY:
      for j in range(BITS_FOR_VERTEX - 1):
        new_path.append(random.randint(0, 1))
    else:
      for j in range(BITS_FOR_VERTEX - 1):
        new_path.append(path[i + j])
