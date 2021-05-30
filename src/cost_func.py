from typing import List, Tuple
from math import exp, log

from graph import Graph


class CostFunc():
  # Set cost to be inxinity
  _cost: float = float('inf')

  def __init__(self,
               path_x: List[int],
               path_y: List[int],
               graph: Graph,
               xi_x: float = 1.,
               xi_y: float = 1.,
               l_x: float = 1.,
               l_y: float = 1.):
    self._path_x = path_x
    self._path_y = path_y
    self._xi_x = xi_x
    self._xi_y = xi_y
    self._l_x = l_x
    self._l_x = l_y
    self._graph = graph
    self._t = self._calc_common_arcs()
    self._arcs = self._get_arcs()

    self._calc_cost()

  def get_cost(self):
    return self._cost

  def _set_cost(self, cost: float):
    self._cost = cost

    return self._cost

  def _calc_cost(self) -> float:
    self._set_cost(self._cost_func() + self._penalise_flow_conservation() +
                   self._penalise_overloadepath_ds() +
                   self._penalise_invalipath_ds())
    return self.get_cost()

  def _cost_func(self) -> float:
    priority_objective = self._t * (self._xi_x + self._xi_y)
    # Num of arcs is equal to num of vertices - 1
    path_x_cost = self._xi_x / (len(self._path_x) - 1)
    path_y_cost = exp(
        self._xi_y *
        sum([log(1. - self._get_used_bandwidth(arc)) for arc in self._arcs]))

    return priority_objective - path_x_cost - path_y_cost

  def _get_used_bandwidth(self, arc: Tuple[int, int]) -> float:
    pass

  def _calc_common_arcs(self) -> int:
    pass

  def _penalise_flow_conservation(self) -> float:
    pass

  def _penalise_overloadepath_ds(self) -> float:
    pass

  def _penalise_invalipath_ds(self) -> float:
    pass

  def _get_arcs(self) -> List[Tuple[int, int]]:
    return [(self._path_y[i], self._path_y[i + 1])
            for i in range(1,
                           len(self._path_y) - 1)]
