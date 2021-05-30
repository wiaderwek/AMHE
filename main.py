from utils import *
from cost_func import CostFunc
from constants import *
from evolution import *


def main():
  g = load_data(
    "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2.xml",
    "D:\\Tomek\\PW-informatyka\\Magisterka\\SEM2\\AMHE\\projekt\\przykladowe_dane\\gen_50_d_2_0_4_1.txt"
  )

  population = g.gen_population()

  print(population)

  population_with_cost = [(population[i], CostFunc(g.get_path(population[i][SHORTEST]), g.get_path(population[i][BEST]), g).get_cost()) for i in range(len(population) - 1)]

  it = 0
  for i in range(100000):
    reproduced_population = reproduce_population(population_with_cost, g)
    mutate(reproduced_population, g)

    rep_population_with_cost = [(reproduced_population[i], CostFunc(g.get_path(reproduced_population[i][SHORTEST]),
                                                     g.get_path(reproduced_population[i][BEST]), g).get_cost()) for i
                            in range(len(reproduced_population) - 1)]

    for pop_mem in rep_population_with_cost:
      population_with_cost.append(pop_mem)

    #[print(population_with_cost[i][1]) for i in range(len(population_with_cost) - 1)]
    population_with_cost = sorted(population_with_cost, key=lambda x: x[1])
    population_with_cost = population_with_cost[:SIZE_OF_POPULATION]

    if i % 1000 == 0:
      print("[Iteration: {}] Best member's function cost: {}".format(it, population_with_cost[0][1]))

    it += 1


if __name__ == "__main__":
  main()
