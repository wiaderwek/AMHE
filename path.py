from typing import List, Tuple
from operator import is_not
from functools import partial


class Path():
  _num_of_correct_links: int

  def __init__(self, path: List[str]) -> None:
    self._path = path
    self._arcs = self._get_arcs(self.get_real_path())
    self._mismatch_list: List[int] = [0] * len(path)

  def __eq__(self, o) -> bool:
    return self._path == o._path

  def __ne__(self, o) -> bool:
      return self._path != o._path

  def __repr__(self) -> str:
      return str(self._path)

  def _get_arcs(self, path: List[str]) -> List[Tuple[str, str]]:
    return [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

  def get_arcs(self):
    return self._arcs

  def get_path(self):
    return self._path

  def get_vertex(self, index) -> str:
    return self._path[index]

  def get_mismatch_list(self):
    return self._mismatch_list

  def set_num_of_correct_links(self, value: int):
    self._num_of_correct_links = value
    return self._num_of_correct_links

  def get_num_of_correct_links(self):
    return self._num_of_correct_links

  def increase_vertex_mismatch_count(self, index):
    self._mismatch_list[index] += 1

    return self._mismatch_list[index]

  def get_num_of_common_arcs(self, arcs: List[Tuple[str, str]]) -> int:
    return len(set(self._arcs).intersection(arcs))

  def get_real_path(self):
    return list(filter(partial(is_not, None), self._path))
