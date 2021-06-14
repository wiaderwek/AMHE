from typing import Tuple
from math import exp, log
from constants import (INVALID_PATH_PENALTY, LOOP_IN_PATH_PENALTY)

from graph import Graph
from path import Path


class CostFunc():
  # Set cost to be infinity
  _cost: float = float('inf')

  def __init__(self,
               path_x: Path,
               path_y: Path,
               graph: Graph,
               xi_x: float = 3.,
               xi_y: float = 1.,):
    self._path_x = path_x
    self._path_y = path_y
    self._xi_x = xi_x
    self._xi_y = xi_y
    self._l_x = graph.get_l_x()
    self._l_x = graph.get_l_y()
    self._graph = graph
    self._t = path_x.get_num_of_common_arcs(path_y.get_arcs())

    self._calc_cost()

  def get_cost(self):
    return self._cost

  def get_common_arcs(self):
    return self._t

  def _set_cost(self, cost: float):
    self._cost = cost

    return self._cost

  def _calc_cost(self) -> float:
    self._set_cost(self._cost_func() + self._penalize_invalid_paths())
    return self.get_cost()

  def _cost_func(self) -> float:

    if len(self._path_x.get_arcs()) == 0 or len(self._path_y.get_arcs()) == 0:
      return self.get_cost()

    priority_objective = self._t * (self._xi_x + self._xi_y)
    path_x_cost = self._xi_x / len(self._path_x.get_arcs())
    path_y_cost = self._xi_y * exp(
        sum([
            log(1. - float(self._get_used_bandwidth(arc)))
            for arc in self._path_y.get_arcs()
        ]))

    return priority_objective - path_x_cost - path_y_cost

  def _get_used_bandwidth(self, arc: Tuple[str, str]) -> float:
    return self._graph.get_arc_bandwitdth(arc)

  def _penalize_invalid_paths(self) -> float:
    penalty = 0.

    num_of_correct_links_x = self._graph.num_of_correct_links(self._path_x)
    num_of_correct_links_y = self._graph.num_of_correct_links(self._path_y)

    # print('[Path x] arcs: {} correct_arcs: {}'.format(len(self._path_x.get_arcs()), num_of_correct_links_x,))
    # print(self._path_x)
    # print('[Path y] arcs: {} correct_arcs: {}'.format(len(self._path_y.get_arcs()), num_of_correct_links_y,))
    # print(self._path_y)
    # raise

    penalty += INVALID_PATH_PENALTY * (
        1 - num_of_correct_links_x / len(self._path_x.get_arcs()))
    penalty += INVALID_PATH_PENALTY * (
        1 - num_of_correct_links_y / len(self._path_y.get_arcs()))

    penalty += LOOP_IN_PATH_PENALTY * (
        1 - len(set(self._path_x.get_real_path())) / len(self._path_x.get_real_path()))
    penalty += LOOP_IN_PATH_PENALTY * (
        1 - len(set(self._path_y.get_real_path())) / len(self._path_y.get_real_path()))

    return penalty

  # def _penalize_flow_disruption(self) -> float:
  #   penalty = 0.
  #   penalty += DISRUPTED_FLOW_PENALTY if self._graph.is_flow_disrupted(
  #       self._path_x) else 0
  #   penalty += DISRUPTED_FLOW_PENALTY if self._graph.is_flow_disrupted(
  #       self._path_y) else 0

  #   return penalty

  # def _penalize_overloadepaths(self) -> float:
  #   penalty = 0.
  #   penalty += OVERLOADED_PATH_PENALTY if self._graph.is_path_overloaded(
  #       self._path_x) else 0
  #   penalty += OVERLOADED_PATH_PENALTY if self._graph.is_path_overloaded(
  #       self._path_y) else 0

  #   return penalty

  # def _penalize_invalid_source_and_destination(self) -> float:
  #   penalty = 0.
  #   penalty += 0 if self._graph.is_source_and_destination_correct(
  #       self._path_x[0],
  #       self._path_x[-1]) else INVALID_SOURCE_AND_DESTINATION_PENALTY
  #   penalty += 0 if self._graph.is_source_and_destination_correct(
  #       self._path_y[0],
  #       self._path_y[-1]) else INVALID_SOURCE_AND_DESTINATION_PENALTY

  #   return penalty
