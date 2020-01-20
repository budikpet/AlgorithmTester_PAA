from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.knapsack.alg_dataclasses import Thing, TaskSA, SolutionSA


class SimulatedAnnealingPenalty(Algorithm):
    """ 
    
    Uses Simulated annealing algorithm. 
    It's a hill climbing algorithm which can accept a worse solution with a certain probability.
    It always accepts better solution if available.
    This probability depends on the size of difference between solutions and current temperature.
    The higher the temperature the more likely the algorithm is to accept a worse solution.

    Dealing with impossible solutions:
        This version uses penalty function to penalize solutions whose weight is heigher than capacity.
    
    """

    def required_click_params(self) -> List[DynamicClickOption]:
        init_temp = DynamicClickOption(name="init_temperature", data_type=float, short_opt="", long_opt="--init-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the starting temperature of SA.")
        cooling = DynamicClickOption(name="cooling", data_type=float, short_opt="", long_opt="--cooling", 
            required=True, doc_help="A float number from interval (0; 1]. Represents the cooling coefficient of SA. Usage: temperature1 = temperature0 * cooling")
        min_temp = DynamicClickOption(name="min_temperature", data_type=float, short_opt="", long_opt="--min-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the minimum temperature of SA. The algorithm ends when this or lower temperature is achieved.")
        cycles = DynamicClickOption(name="cycles", data_type=int, short_opt="", long_opt="--cycles", 
            required=True, doc_help="An int number from interval (0; +inf). Represents the number of internal cycles of SA that are done before cooling occurs.")
        
        return [init_temp, cooling, min_temp, cycles]

    def get_name(self) -> str:
        return "SAPenalty"

    def get_columns(self, show_time: bool = True) -> List[str]:
        columns: List[str] = [
            "id",
            "item_count",
            "algorithm_name",
            "init_temperature",
            "cooling",
            "min_temperature",
            "cycles",
            "found_value",
            "elapsed_configs",
            "elapsed_time",
            "things"
        ]

        return columns

    def get_sums(self, task: TaskSA, solution: np.ndarray):
        cost, weight = 0, 0

        # Get sums of weights and costs
        for (index, value) in enumerate(solution):
            if value == 1:
                curr_thing: Thing = task.things[index]
                cost += curr_thing.cost
                weight += curr_thing.weight

        return cost, weight

    def get_fitness(self, task: TaskSA, solution: SolutionSA):
        # The higher cost the better. If weight > capacity then the fitness value is negative.

        return (task.capacity - solution.sum_weight + 1) * solution.sum_cost

    def initial_solution(self, task: TaskSA) -> SolutionSA:
        solution: np.ndarray = np.zeros((task.count), dtype=int)
        remaining_capacity = task.capacity

        # Find solution
        weight, cost = 0, 0
        for index, thing in enumerate(task.things):
            if thing.weight <= remaining_capacity:
                remaining_capacity -= thing.weight
                solution[index] = 1
                weight += thing.weight
                cost += thing.cost

            if remaining_capacity <= 0:
                break

        return SolutionSA(solution, cost, weight)

    def change_solution(self, task: TaskSA, solution: SolutionSA, index: int):
        new_value: int = (solution[index] + 1) % 2
        solution[index] = new_value
        curr_thing: Thing = task.things[index]

        if new_value == 1:
            solution.sum_cost += curr_thing.cost
            solution.sum_weight += curr_thing.weight
        else:
            solution.sum_cost -= curr_thing.cost
            solution.sum_weight -= curr_thing.weight


    def get_solution(self, task: TaskSA) -> (SolutionSA, int):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        curr_sol: SolutionSA = self.initial_solution(task)
        curr_fitness: float = self.get_fitness(task, curr_sol)

        random.seed(20191219)

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1
                index: int = random.randint(0, task.count-1)
                curr_thing: Thing = task.things[index]

                # Try neighbour solution
                self.change_solution(task, curr_sol, index)
                new_fitness: float = self.get_fitness(task, curr_sol)

                if new_fitness > curr_fitness:
                    # Neighbour solution is better, accept it
                    curr_fitness = new_fitness

                elif exp( (new_fitness - curr_fitness) / curr_temp) >= random.random():
                    # Simulated Annealing condition. 
                    # Enables us to accept worse solution with a certain probability
                    curr_fitness = new_fitness

                else:
                    # Change the solution back
                    self.change_solution(task, curr_sol, index)
                print

            curr_temp *= task.cooling_coefficient

        return curr_sol, sol_cntr
 
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSA = TaskSA(context, parsed_data=parsed_data)
        task.things = sorted(task.things, key=lambda thing: thing.cost/(thing.weight + 1), reverse=True)
        
        solution, solution_cntr = self.get_solution(task)

        # Pass solution
        out_things: np.ndarray = np.zeros((task.count), dtype=int)
        for index, value in enumerate(solution.solution):
            if value == 1:
                thing: Thing = task.things[index]
                out_things[thing.position] = 1

        parsed_data.update({
            "found_value": solution.sum_cost,
            "elapsed_configs": solution_cntr,
            "things": solution.solution
        })

        return parsed_data