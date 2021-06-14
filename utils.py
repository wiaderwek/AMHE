import random
import xml.etree.ElementTree as ET
import os

from graph import Graph
from constants import BITS_FOR_VERTEX


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


# g = load_data(
#     "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2.xml",
#     "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2_0_4_1.txt"
# )
#
# print(g.is_path_correct(['N1', 'N2', 'N3']))
# print(g.is_path_correct(['N1', 'N39', 'N2']))

# def find_paths(ver1, ver2):


def gen_random_path(size):
  path = []
  for i in range(BITS_FOR_VERTEX * size):
    path.append(random.randint(0, 1))

  return path

def get_test_file_pairs(data_path):
  test_data = dict()
  for xml in os.listdir(data_path):
    if xml.endswith(".xml"):
      test_data[os.path.join(data_path, xml)] = list()
      for txt in os.listdir(data_path):
        if txt.endswith(".txt") and txt.startswith(os.path.splitext(xml)[0]):
          test_data[os.path.join(data_path, xml)].append(os.path.join(data_path, txt))

  return test_data


# population = gen_population(g)
# print("Number of vertices: {}".format(g.get_number_of_vertices()))
# print(get_member_as_vertices(population[0], g))
#
# # for member in population:
# #     vertices = get_member_as_vertices(member, g)
# #
# #     if not all(x is None for x in vertices[SHORTEST]) or not all(x is None for x in vertices[BEST]):
# #         print(vertices)
#
# reproduced_members = reproduce_members(population[0], population[1])
# print("Reproduced members: {}".format(reproduced_members))
# mutated_members = mutate(reproduced_members)
# print("Mutated members: {}".format(mutated_members))
