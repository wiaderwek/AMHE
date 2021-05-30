from typing import List, Tuple
from math import exp, log
from constants import (DISRUPTED_FLOW_PENALTY, INVALID_PATH_PENALTY,
                       OVERLOADED_PATH_PENALTY)

from graph import Graph


class CostFunc():
  # Set cost to be infinity
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
    self._arcs_x = self._get_arcs(self._path_x)
    self._arcs_y = self._get_arcs(self._path_y)

    self._calc_cost()

  def get_cost(self):
    return self._cost

  def _set_cost(self, cost: float):
    self._cost = cost

    return self._cost

  def _calc_cost(self) -> float:
    self._set_cost(self._cost_func() + self._penalize_flow_disruption() +
                   self._penalize_overloadepaths() +
                   self._penalize_invalipaths())
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
    return self._graph.get_arc_bandwitdth(arc)

  def _calc_common_arcs(self) -> int:
    num_of_common_arcs = 0

    for arc in self._arcs_x:
      num_of_common_arcs += 1 if arc in self._arcs_y else 0

    return num_of_common_arcs

  def _penalize_flow_disruption(self) -> float:
    penalty = 0.
    penalty += DISRUPTED_FLOW_PENALTY if self._graph.is_flow_disrupted(
        self._path_x) else 0
    penalty += DISRUPTED_FLOW_PENALTY if self._graph.is_flow_disrupted(
        self._path_y) else 0

    return penalty

  def _penalize_overloadepaths(self) -> float:
    penalty = 0.
    penalty += OVERLOADED_PATH_PENALTY if self._graph.is_path_overloaded(
        self._path_x) else 0
    penalty += OVERLOADED_PATH_PENALTY if self._graph.is_path_overloaded(
        self._path_y) else 0

    return penalty

  def _penalize_invalipaths(self) -> float:
    penalty = 0.
    penalty += INVALID_PATH_PENALTY if self._graph.is_path_correct(
        self._path_x) else 0
    penalty += INVALID_PATH_PENALTY if self._graph.is_path_correct(
        self._path_y) else 0

    return penalty

  def _get_arcs(self, path: List[int]) -> List[Tuple[int, int]]:
    return [(path[i], path[i + 1]) for i in range(1, len(path) - 1)]
