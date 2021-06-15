from constants import BEST, SHORTEST
from absl import app, flags
import datetime

from save_result import save_result
from utils import is_dir_correct, load_data, get_test_file_pairs
from evolution import Evolution

FLAGS = flags.FLAGS

flags.DEFINE_string('data_dir',
                    default='data',
                    help='Path to input file containing dataset.')
flags.DEFINE_string(
    'output_dir',
    default='results',
    help='Path to output file where clastering results will be stored.')
flags.DEFINE_string(
    'graph_path',
    default=None,
    help='Path to the graph for which algorithm will be executed. ' +
    'If skiped prediction will be made for all graphs in data dir')
flags.DEFINE_integer('start_index',
                     default=None,
                     help='Minimal index of test data for graph.')
flags.DEFINE_integer('stop_index',
                     default=None,
                     help='Maximal index of test data for graph.')


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
      test_case_idx = test_case.split('.')[0].split('_')[-1]

      if test_case_idx == 'config':
        continue
      elif (FLAGS.start_index is not None and
            int(test_case_idx) < FLAGS.start_index or
            FLAGS.stop_index is not None and
            int(test_case_idx) > FLAGS.stop_index):  # noqa: E125
        continue

      g = load_data(graph, test_case)
      timestamp = str(datetime.datetime.now())
      evol_alg = Evolution(g)

      (exec_time, best, best_iterations, iter, is_shortest_path_correct,
       is_best_path_correct) = evol_alg.run()

      result_file_name = graph.split('/')[-1].split('.')[0] + '_result'
      source = g.get_source()
      target = g.get_target()
      save_result(FLAGS.output_dir, result_file_name, timestamp, source, target,
                  exec_time, iter, best_iterations, best[1],
                  is_shortest_path_correct, is_best_path_correct,
                  best[0][SHORTEST], best[0][BEST])


if __name__ == '__main__':
  app.run(main)
