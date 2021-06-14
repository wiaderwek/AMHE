from utils import load_data, get_test_file_pairs
from evolution import Evolution


def main():
  test_files = get_test_file_pairs("../")
  # for links, demands_list in test_files.items():
  #   for demands in demands_list:
  #     g = load_data(links, demands)
  #     evol_alg = Evolution(g)
  #
  #     evol_alg.run()

  g = load_data("../gen_150_d_2.xml", "../gen_150_d_2_0_4_1.txt")
  evol_alg = Evolution(g)

  evol_alg.run()
  # first_population = g.gen_first_population()

  # # print(population)

  # population_with_cost = [
  #     (first_population[i],
  #      CostFunc(g.get_path(first_population[i][SHORTEST]),
  #               g.get_path(first_population[i][BEST]), g).get_cost())
  #     for i in range(len(first_population))
  # ]
  # # print("Population: {}".format(population_with_cost))
  # population_with_cost = sorted(population_with_cost, key=lambda x: x[1])
  # population = Evolution(population_with_cost[:SIZE_OF_POPULATION])

  # it = 0
  # for i in range(100000):
  #   reproduced_population = population.reproduce_population()

  #   population.mutate(reproduced_population)

  #   rep_population_with_cost = [
  #       (reproduced_population[i],
  #        CostFunc(g.get_path(reproduced_population[i][SHORTEST]),
  #                 g.get_path(reproduced_population[i][BEST]), g).get_cost())
  #       for i in range(len(reproduced_population) - 1)
  #   ]

  #   for pop_mem in rep_population_with_cost:
  #     population_with_cost.append(pop_mem)

  #   # [print(population_with_cost[i][1]) for i in range(len(population_with_cost) - 1)]
  #   population_with_cost = sorted(population_with_cost, key=lambda x: x[1])
  #   population_with_cost = population_with_cost[:SIZE_OF_POPULATION]
  #   if i % 100 == 0:
  #     print(
  #         "[Iteration: {}] Best member's function cost: {} ([correct / all] x: {} / {}, y: {} / {})"
  #         .format(
  #             it, population_with_cost[0][1],
  #             g.num_of_correct_links(
  #                 g.get_path(population_with_cost[0][0][SHORTEST])),
  #             len(g.get_path(population_with_cost[0][0][SHORTEST])) - 1,
  #             g.num_of_correct_links(
  #                 g.get_path(population_with_cost[0][0][BEST])),
  #             len(g.get_path(population_with_cost[0][0][BEST])) - 1))
  #     print(population_with_cost[0][0])

  #   it += 1


if __name__ == "__main__":
  main()
