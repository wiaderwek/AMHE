from typing import List


def save_result(result_dir: str, file_name: str, demand: str, timestamp: str,
                exec_time: float, iterations: int, best_iterations: int, cost: float,
                shortest_path: List[str], best_path: List[str]):
  row = ', '.join([
      demand, timestamp,
      str(exec_time),
      str(iterations),
      str(best_iterations),
      str(cost),
      str(shortest_path),
      str(best_path)
  ])

  with open(result_dir + '/' + file_name + '.csv', 'a') as fd:
    fd.write(row + '\n')
