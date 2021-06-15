from path import Path
from operator import is_not
from functools import partial
import random
from typing import Dict, List, Tuple

from constants import (BEST, BITS_FOR_VERTEX, EMPTY_VERTEX, SHORTEST,
                       SIZE_OF_FIRST_POPULATION, SIZE_OF_POPULATION, NONE_PROB,
                       MAX_PATH_LENGTH)


class Graph:

  def __init__(self, links, file_content: Dict[str, str]):
    self._links = self.load_links_to_map(links)
    self._metadata, self._demands = self.parse_file_content(file_content)
    self._source = self._metadata['source']
    self._target = self._metadata['target']

    self._vertices_for_generation = list(
        filter(lambda x: x not in [self._source, self._target],
               list(self._links.keys())))
    for _ in range(int(len(self._vertices_for_generation) * EMPTY_VERTEX)):
      self._vertices_for_generation.append(None)

    random.shuffle(self._vertices_for_generation)

  def parse_file_content(self, file_content: Dict[str, str]):
    demands: List[str] = []
    metadata: Dict[str, str] = {}
    for key in file_content:
      if key not in ['Lx', 'Ly'] and key.startswith('L'):
        demands.append(key)
      else:
        metadata[key] = file_content[key]

    return metadata, demands

  def is_path_correct(self, path: Path):
    for i in range(len(path.get_path()) - 1):
      if path.get_vertex(i + 1) not in self._links[path.get_vertex(i)]:
        return False

    return True

  def num_of_correct_links(self, path: Path):
    '''WARNING: Watch out for more than one execution on the same path '''
    num_of_correct_links = 0
    v_1 = None
    v_2 = None
    idx_1 = None

    for i in range(len(path.get_path()) - 1):
      if path.get_vertex(i) is not None:
        v_1 = path.get_vertex(i)
        idx_1 = i

      if path.get_vertex(i + 1) is None:
        continue

      v_2 = path.get_vertex(i + 1)

      if v_2 not in self._links[v_1]:
        path.increase_vertex_mismatch_count(idx_1)
        path.increase_vertex_mismatch_count(i + 1)
      else:
        num_of_correct_links += 1

    path.set_num_of_correct_links(num_of_correct_links)
    # if (num_of_correct_links != 0):
    #   print('----------------------------------\n')
    #   print(path.get_path())
    #   print(path.get_mismatch_list())
    #   print(num_of_correct_links)
    #   raise

    return num_of_correct_links

  def is_path_overloaded(self, path: List[str]) -> bool:
    pass

  def is_flow_disrupted(self, path: List[str]) -> bool:
    pass

  def is_source_and_destination_correct(self, source: str,
                                        destination: str) -> bool:
    return source == self._source and destination == self._target

  def get_arc_bandwitdth(self, arc: Tuple[str, str]) -> float:
    return self._metadata['current_load']

  def get_l_x(self) -> float:
    return self._metadata['Lx']

  def get_l_y(self) -> float:
    return self._metadata['Ly']

  def get_demands(self) -> List[str]:
    return self._demands

  def load_links_to_map(self, links):
    graph = dict()
    for link in links:
      if link[0].text not in graph:
        graph[link[0].text] = set()
      if link[1].text not in graph:
        graph[link[1].text] = set()

      graph[link[0].text].add(link[1].text)
      graph[link[1].text].add(link[0].text)

    # print(graph)
    return graph

  def load_demands(self, demands):
    print(demands)

  def get_number_of_vertices(self):
    return len(self._links)

  def get_vertex_by_index(self, idx):
    if idx < self.get_number_of_vertices():
      return list(self._links.keys())[idx]
    return

  def get_path(self, path: List[str]):
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
          number += path[i + j] * 2**(BITS_FOR_VERTEX - j - 1)
        except IndexError:
          print("Path: {}, index: {}, len: {}".format(path, i + j, len(path)))
          raise
      path_as_vertices.append(self.get_vertex_by_index(number))

    return path_as_vertices

  def gen_population(self) -> List[Dict[str, Path]]:
    population = [
        self.gen_population_member() for _ in range(SIZE_OF_POPULATION)
    ]

    return population

  def gen_first_population(self) -> List[Dict[str, Path]]:
    population = [
        self.gen_population_member() for _ in range(SIZE_OF_FIRST_POPULATION)
    ]

    return population

  def gen_population_member(self):
    member: Dict[str, Path] = dict()
    # member[SHORTEST] = utils.gen_random_path(self.get_number_of_vertices())
    # member[BEST] = utils.gen_random_path(self.get_number_of_vertices())
    member[SHORTEST] = Path(self.gen_random_member(MAX_PATH_LENGTH))
    member[BEST] = Path(self.gen_random_member(MAX_PATH_LENGTH))
    return member

  def gen_random_member(self, size):
    member = list()
    member.append(self._source)
    for i in range(size - 2):
      member.append(self.get_random_vertex())
    member.append(self._target)

    return member

  def get_random_vertex(self):
    return random.choice(self._vertices_for_generation)

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
      raise BaseException("Error: len: {}, path: {}".format(
          len(path_as_bits), path_as_bits))
    return path_as_bits

  def get_mutate_vertex(self, vertex):
    if vertex is None:
      return self.get_random_vertex()
    neighbors = self._links[vertex]
    neighbors = list(
        filter(lambda x: x not in [self._source, self._target], neighbors))
    neighbors.append(None)
    [neighbors.append(None) for _ in range(int(NONE_PROB * len(neighbors)))]

    return random.choice(neighbors)
