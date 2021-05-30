import random
import xml.etree.ElementTree as ET

from graph import Graph
from constants import (BEST, BITS_FOR_VERTEX, SHORTEST, SIZE_OF_POPULATION)
from evolution import reproduce_members, mutate


def load_data(graph_path, demands_path):
  links = load_xml(graph_path)
  demands = load_txt(demands_path)
  return Graph(links, demands)


def load_xml(graph_path):
  graph = ET.parse(graph_path)
  return graph.getroot()[0][0]


def load_txt(demands_path):
  with open(demands_path) as f:
    content = f.readlines()
    content = [x.strip() for x in content]

    return dict((v.split(',')) for v in content)


g = load_data(
    "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2.xml",
    "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2_0_4_1.txt"
)

print(g.is_path_correct(['N1', 'N2', 'N3']))
print(g.is_path_correct(['N1', 'N39', 'N2']))

# def find_paths(ver1, ver2):


def gen_population(graph):
  population = [
      gen_population_member(graph) for _ in range(SIZE_OF_POPULATION - 1)
  ]

  return population


def gen_population_member(graph):
  member = dict()
  member[SHORTEST] = gen_random_path(graph.get_number_of_vertices())
  member[BEST] = gen_random_path(graph.get_number_of_vertices())

  return member


def gen_random_path(size):
  path = []
  for i in range(BITS_FOR_VERTEX * size - 1):
    path.append(random.randint(0, 1))
  return path


def get_member_as_vertices(member, graph):
  return {
      SHORTEST: get_path_as_numbers(member[SHORTEST], graph),
      BEST: get_path_as_numbers(member[BEST], graph)
  }


def get_path_as_numbers(path, graph):
  path_as_vertices = []
  for i in range(0, len(path) - 1, BITS_FOR_VERTEX):
    number = 0
    for j in range(BITS_FOR_VERTEX - 1):
      number += path[i + j] * 2**(BITS_FOR_VERTEX - j - 1)
    path_as_vertices.append(graph.get_vertex_by_index(number))

  return path_as_vertices


population = gen_population(g)
print("Number of vertices: {}".format(g.get_number_of_vertices()))
print(get_member_as_vertices(population[0], g))

# for member in population:
#     vertices = get_member_as_vertices(member, g)
#
#     if not all(x is None for x in vertices[SHORTEST]) or not all(x is None for x in vertices[BEST]):
#         print(vertices)

reproduced_members = reproduce_members(population[0], population[1])
print("Reproduced members: {}".format(reproduced_members))
mutated_members = mutate(reproduced_members)
print("Mutated members: {}".format(mutated_members))
