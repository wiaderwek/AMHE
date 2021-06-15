from constants import BEST, SHORTEST
from absl import app, flags
import datetime

from save_result import save_result
from utils import is_dir_correct, load_data, get_test_file_pairs
from evolution import Evolution

FLAGS = flags.FLAGS

flags.DEFINE_string('data_dir',
                    default='./data',
                    help='Path to input file containing dataset.')
flags.DEFINE_string(
    'output_dir',
    default='./results',
    help='Path to output file where clastering results will be stored.')
flags.DEFINE_string(
    'graph_path',
    default=None,
    help='Path to the graph for which algorithm will be executed. ' +
    'If skiped prediction will be made for all graphs in data dir')


def check_flags():
  if not is_dir_correct(FLAGS.data_dir):
    raise AttributeError(
        'Provided data_dir `{}` is not a valid directory'.format(
            FLAGS.data_dir))
  if not is_dir_correct(FLAGS.output_dir):
    raise AttributeError(
        'Provided output_dir `{}` is not a valid directory'.format(
            FLAGS.output_dir))


def main(_):
  check_flags()
  test_files = get_test_file_pairs(FLAGS.data_dir)

  for graph in test_files:
    if FLAGS.graph_path is not None and graph != FLAGS.graph_path:
      continue

    for test_case in test_files[graph]:
      g = load_data(graph, test_case)
      for demand in g.get_demands():
        timestamp = str(datetime.datetime.now())

        evol_alg = Evolution(g)
        exec_time, best, best_iterations, iter = evol_alg.run()

        result_file_name = test_case.split('/')[-1].split('.')[0] + '_result'
        print(result_file_name)
        save_result(FLAGS.output_dir, result_file_name, demand, timestamp,
                    exec_time, iter, best_iterations, best[1],
                    best[0][SHORTEST], best[0][BEST])


if __name__ == '__main__':
  app.run(main)
