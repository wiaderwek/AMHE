import random
from typing import Dict, List
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


def gen_random_path(size):
  path = []
  for i in range(BITS_FOR_VERTEX * size):
    path.append(random.randint(0, 1))

  return path


def get_test_file_pairs(data_path):
  test_data: Dict[str, List[str]] = dict()
  for xml in os.listdir(data_path):
    if xml.endswith(".xml"):
      test_data[os.path.join(data_path, xml)] = list()
      for txt in os.listdir(data_path):
        if txt.endswith(".txt") and txt.startswith(os.path.splitext(xml)[0]):
          test_data[os.path.join(data_path,
                                 xml)].append(os.path.join(data_path, txt))

  return test_data


def is_dir_correct(path: str):
  return os.path.isdir(path)
