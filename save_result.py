from typing import List
from constants import (
    DISRUPTED_FLOW_PENALTY, EMPTY_VERTEX, INVALID_PATH_PENALTY,
    INVALID_SOURCE_AND_DESTINATION_PENALTY, LOOP_IN_PATH_PENALTY,
    MAX_BEST_OCCURRENECES, MAX_ITER, MAX_PATH_LENGTH, MUTATE_GEN_PROBABILITY,
    MUTATE_MEMBER_PROBABILITY, MUTATE_MISSMATCHED_GEN_PROBABILITY_WEIGHT,
    NONE_PROB, OVERLOADED_PATH_PENALTY, REPRODUCTION_POINT_DIVIDER,
    REPRODUCTION_PROBABILITY, SIZE_OF_FIRST_POPULATION, SIZE_OF_POPULATION)


def save_result(result_dir: str, file_name: str, timestamp: str, source: str,
                target: str, exec_time: float, iterations: int,
                best_iterations: int, cost: float, is_shortest_path_correct,
                is_best_path_correct, shortest_path: List[str],
                best_path: List[str]):
  row = ', '.join([
      timestamp, source, target,
      str(exec_time),
      str(iterations),
      str(best_iterations),
      str(cost),
      str(is_shortest_path_correct),
      str(is_best_path_correct),
      str(shortest_path),
      str(best_path),
      str(MAX_ITER),
      str(MAX_BEST_OCCURRENECES),
      str(SIZE_OF_FIRST_POPULATION),
      str(SIZE_OF_POPULATION),
      str(REPRODUCTION_PROBABILITY),
      str(REPRODUCTION_POINT_DIVIDER),
      str(MUTATE_MEMBER_PROBABILITY),
      str(MUTATE_GEN_PROBABILITY),
      str(MUTATE_MISSMATCHED_GEN_PROBABILITY_WEIGHT),
      str(NONE_PROB),
      str(EMPTY_VERTEX),
      str(INVALID_PATH_PENALTY),
      str(LOOP_IN_PATH_PENALTY),
      str(INVALID_SOURCE_AND_DESTINATION_PENALTY),
      str(OVERLOADED_PATH_PENALTY),
      str(DISRUPTED_FLOW_PENALTY),
      str(MAX_PATH_LENGTH)
  ])

  with open(result_dir + '/' + file_name + '.csv', 'a') as fd:
    fd.write(row + '\n')
