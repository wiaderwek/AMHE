from typing import List, Tuple
import utils
from operator import is_not
from functools import partial
from constants import *
import random


class Graph:

  def __init__(self, links, demands):
    self._links = self.load_links_to_map(links)
    self._demands = demands
    self._source = 'N43'
    self._target = 'N33'

    self._vertices_for_generation = list(filter(lambda x: x not in [self._source, self._target], list(self._links.keys())))
    self._vertices_for_generation.append(None)


  def is_path_correct(self, path):
    for i in range(len(path) - 1):
      if path[i + 1] not in self._links[path[i]]:
        return False

    return True

  def is_path_overloaded(self, path: List[int]) -> bool:
    pass

  def is_flow_disrupted(self, path: List[int]) -> bool:
    pass

  def is_source_and_destination_correct(self, source: int, destination: int) -> bool:
    return True

  def get_arc_bandwitdth(self, arc: Tuple[int, int]) -> float:
    return 0.2

  def load_links_to_map(self, links):
    graph = dict()
    for link in links:
      if link[0].text not in graph:
        graph[link[0].text] = set()
      if link[1].text not in graph:
        graph[link[1].text] = set()

      graph[link[0].text].add(link[1].text)
      graph[link[1].text].add(link[0].text)

    print(graph)
    return graph

  def get_number_of_vertices(self):
    return len(self._links)

  def get_vertex_by_index(self, idx):
    if idx < self.get_number_of_vertices():
      return list(self._links.keys())[idx]
    return

  def get_path(self, path):
    return list(filter(partial(is_not, None), path))

  def get_member_as_vertices(self, member):
    return {
      SHORTEST: self.get_path_as_numbers(member[SHORTEST]),
      BEST: self.get_path_as_numbers(member[BEST])
    }

  def get_path_as_numbers(self, path):
    path_as_vertices = []
    for i in range(0, len(path) - 1, BITS_FOR_VERTEX):
      number = 0
      for j in range(BITS_FOR_VERTEX - 1):
        try:
          number += path[i + j] * 2 ** (BITS_FOR_VERTEX - j - 1)
        except:
          print("Path: {}, index: {}, len: {}".format(path, i+j, len(path)))
          raise
      path_as_vertices.append(self.get_vertex_by_index(number))

    return path_as_vertices

  def gen_population(self):
    population = [
      self.gen_population_member() for _ in range(SIZE_OF_POPULATION)
    ]

    return population

  def gen_population_member(self):
    member = dict()
    # member[SHORTEST] = utils.gen_random_path(self.get_number_of_vertices())
    # member[BEST] = utils.gen_random_path(self.get_number_of_vertices())
    member[SHORTEST] = self.gen_random_member(self.get_number_of_vertices())
    member[BEST] = self.gen_random_member(self.get_number_of_vertices())

    return member

  def gen_random_member(self, size):
    member = list()
    member.append(self._source)
    for i in range(size - 2):
      member.append(random.choice(self._vertices_for_generation))
    member.append(self._target)

    return member

  def get_path_as_bits(self, path):
    path_as_bits = list()

    for vertex in path:
      if vertex is None:
        for _ in range(BITS_FOR_VERTEX):
          path_as_bits.append(1)
      else:
        index = list(self._links.keys()).index(vertex)
        for bit in '{0:08b}'.format(index):
          path_as_bits.append(int(bit))

    if len(path_as_bits) % 8 != 0:
      raise BaseException("Error: len: {}, path: {}".format(len(path_as_bits), path_as_bits))
    return path_as_bits
