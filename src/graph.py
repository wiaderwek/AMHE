from typing import List, Tuple


class Graph:

  def __init__(self, links, demands):
    self._links = self.load_links_to_map(links)
    self._demands = demands

  def is_path_correct(self, path):
    for i in range(len(path) - 1):
      if path[i + 1] not in self._links[path[i]]:
        return False

    return True

  def is_path_overloaded(self, path: List[int]) -> bool:
    pass

  def is_flow_disrupted(self, path: List[int]) -> bool:
    pass

  def get_arc_bandwitdth(self, arc: Tuple[int, int]) -> float:
    pass

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
    return None
