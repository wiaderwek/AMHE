from cost_func import CostFunc
import random
from typing import Dict, List, Tuple

from constants import (BEST, MAX_ITER, MUTATE_GEN_PROBABILITY,
                       MUTATE_MEMBER_PROBABILITY,
                       MUTATE_MISSMATCHED_GEN_PROBABILITY_WEIGHT,
                       REPRODUCTION_POINT_DIVIDER, REPRODUCTION_PROBABILITY,
                       SHORTEST, SIZE_OF_POPULATION)
from graph import Graph
from path import Path


class Evolution():
  _population: List[Tuple[Dict[str, Path], float]]

  def __init__(self, graph: Graph) -> None:
    self._graph = graph

  # ---------------------------------- main loop ---------------------------------
  def run(self):
    self._create_first_population()

    for iter in range(MAX_ITER):

      self._append_new_population(
          self._add_cost(self._mutate(self._reproduce_population())))
      self._sort_and_crop_population()
      self._log(iter)

  # ---------------------------------- /main loop ---------------------------------

  def _add_cost(self, population: List[Dict[str, Path]]):
    # print('\n')
    # print(population[1][SHORTEST])
    # raise
    return [(population[i],
             CostFunc(population[i][SHORTEST], population[i][BEST],
                      self._graph).get_cost()) for i in range(len(population))]

  def _create_first_population(self):
    first_population = self._graph.gen_first_population()

    population_with_cost = self._add_cost(first_population)

    # print("Population: {}".format(population_with_cost))
    population_with_cost = sorted(population_with_cost, key=lambda x: x[1])

    self._population = population_with_cost[:SIZE_OF_POPULATION]

  def _append_new_population(self, new_population: List[Tuple[Dict[str, Path],
                                                              float]]):
    for new_member in new_population:
      self._population.append(new_member)

  def _sort_and_crop_population(self):
    self._population = sorted(self._population, key=lambda x: x[1])
    self._population = self._population[:SIZE_OF_POPULATION]

  def _reproduce_population(self) -> List[Dict[str, Path]]:
    reproduced_population: List[Dict[str, Path]] = []

    # TODO: nie powinno tu być stepu co 2?
    for i in range(len(self._population) - 1):
      rep_mem1, rep_mem2 = self._reproduce_members(self._population[i][0],
                                                   self._population[i + 1][0])
      reproduced_population.append(rep_mem1)
      reproduced_population.append(rep_mem2)

    return reproduced_population

  def _reproduce_members(self, first_member: Dict[str, Path],
                         second_member: Dict[str, Path]):
    first_shortes, second_shortest = self._reproduce_path(
        first_member[SHORTEST].get_path(), second_member[SHORTEST].get_path())
    first_best, second_best = self._reproduce_path(
        first_member[BEST].get_path(), second_member[BEST].get_path())

    return {
        SHORTEST: Path(first_shortes),
        BEST: Path(first_best)
    }, {
        SHORTEST: Path(second_shortest),
        BEST: Path(second_best)
    }

  def _reproduce_path(self, first_path: List[str], second_path: List[str]):
    if random.randint(0, 100) <= REPRODUCTION_PROBABILITY:

      indexes = set()
      reproduced_path1 = [
          self._graph.get_random_vertex() for _ in range(len(first_path))
      ]
      reproduced_path2 = [
          self._graph.get_random_vertex() for _ in range(len(first_path))
      ]

      while True:
        indexes.add(random.randint(0, len(first_path) - 1))

        if len(indexes) >= int(len(first_path) / REPRODUCTION_POINT_DIVIDER):
          break

      iteration = 0
      indexes_sorted = sorted(indexes)
      for i in range(len(first_path)):
        if iteration < len(indexes) and i >= indexes_sorted[iteration]:
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

  def _mutate(self, reproduced_members: List[Dict[str, Path]]):
    for i in range(len(reproduced_members)):
      if random.randint(0, 100) <= MUTATE_MEMBER_PROBABILITY:
        reproduced_members[i][SHORTEST] = self._mutate_path(
            reproduced_members[i][SHORTEST])
        reproduced_members[i][BEST] = self._mutate_path(
            reproduced_members[i][BEST])

    return reproduced_members

  def _mutate_path(self, path: Path):
    old_path = path.get_path()
    missmatch_list = path.get_mismatch_list()
    new_path = []
    new_path.append(old_path[0])
    for i in range(1, len(old_path) - 1, 1):
      missmatch_penalty = MUTATE_MISSMATCHED_GEN_PROBABILITY_WEIGHT * missmatch_list[
          i]
      mutation_probability = min(MUTATE_GEN_PROBABILITY + missmatch_penalty,
                                 100)
      if random.randint(0, 100) <= mutation_probability:
        new_path.append(self._graph.get_mutate_vertex(old_path[i]))
      else:
        new_path.append(old_path[i])
    new_path.append(old_path[len(old_path) - 1])

    return Path(new_path)

  def _log(self, iter):
    if iter % 100 == 0:
      print(
          "[Iteration: {}] Best member's function cost: {} ([correct / all ] x: {} / {}, y: {} / {}); Common: {}"
          .format(
              iter, self._population[0][1],
              self._population[0][0][SHORTEST].get_num_of_correct_links(),
              len(
                  self._graph.get_path(
                      self._population[0][0][SHORTEST].get_arcs())),
              self._population[0][0][BEST].get_num_of_correct_links(),
              len(self._graph.get_path(
                  self._population[0][0][BEST].get_arcs())),
              self._population[0][0][SHORTEST].get_num_of_common_arcs(
                  self._population[0][0][BEST].get_arcs())))
      print("    [SHORTEST]:{}".format(
          self._population[0][0][SHORTEST].get_path()))
      print("    [SHORTEST]:{}".format(
          self._population[0][0][SHORTEST].get_mismatch_list()))
      print("    [BEST]:{}".format((self._population[0][0][BEST].get_path())))
      print("    [BEST]:{}".format(
          self._population[0][0][BEST].get_mismatch_list()))
