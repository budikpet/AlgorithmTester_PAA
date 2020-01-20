from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.sat.alg_dataclasses import TaskSAT, SolutionSA, base_columns
from package_algorithms.sat.sa_sat_v1 import SimulatedAnnealing_SAT_V1
import csa_sat

class SimulatedAnnealing_SAT_V2(SimulatedAnnealing_SAT_V1):
    """ 
    Version 2 of SA algorithm for SAT problem.
    
    Uses a temperature reset feature. The temperature resets to initial temperature if the found solution is not valid.
    
    """

    def get_name(self) -> str:
        return "SA_SAT_V2"

    def try_new_solution(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA, curr_temp: float):
        """
        Generates neighbour solution. 
        
        Arguments:
            task {TaskSAT} -- [description]
            best_sol {SolutionSA} -- Best solution ever found.
            curr_sol {SolutionSA} -- Currently used solution.
            neighbour_sol {SolutionSA} -- Solution used to contain newly generated neighbour solution.
            curr_temp {float} -- Current temperature.
        """
        
        # Try neighbour solution
        self.get_new_neighbour(task, neighbour_sol)

        if self.is_new_sol_better(neighbour_sol, curr_sol):
            # Neighbour solution is better, accept it
            curr_sol.copy(neighbour_sol)

            if self.is_new_sol_better(curr_sol, best_sol):
                best_sol.copy(curr_sol)

        else:
            if neighbour_sol.is_valid and curr_sol.is_valid:
                # Both solutions valid
                if exp( (neighbour_sol.sum_weight - curr_sol.sum_weight) / curr_temp) > random.random():
                    # Accept worse solution - solution with less sum_weight, because both solutions are valid
                    curr_sol.copy(neighbour_sol)
                else:
                    # Change the solution back
                    neighbour_sol.copy(curr_sol)
            elif (not curr_sol.is_valid) and exp( (neighbour_sol.num_of_satisfied_clauses - curr_sol.num_of_satisfied_clauses) / curr_temp) > random.random():
                # Accept worse solution - solution with less clauses, because neither solution is valid
                curr_sol.copy(neighbour_sol)
            else:
                # Change the solution back
                neighbour_sol.copy(curr_sol)
        print

    def compute_solution_with_evo(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA):
        curr_temp: float = 0
        sol_cntr: int = 0
        retry_cnt: int = 0
        cycles: int = 0
        
        with open(task.evo_filepath, "w") as evo_file:
            while ((best_sol.is_valid == False) and (retry_cnt < task.max_retry_attempts)) or (retry_cnt == 0):
                retry_cnt += 1
                curr_temp = task.init_temp
                cycles = retry_cnt*task.cycles

                while curr_temp > task.min_temp:
                    for _ in range(task.cycles):
                        sol_cntr += 1

                        self.try_new_solution(task, best_sol, curr_sol, neighbour_sol, curr_temp)
                        evo_file.write(f'{task.sol_file_name} {curr_sol.num_of_satisfied_clauses} {curr_sol.sum_weight}\n')

                    curr_temp *= task.cooling

        return best_sol, sol_cntr, retry_cnt

    def compute_solution(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA):
        curr_temp: float = 0
        sol_cntr: int = 0
        retry_cnt: int = 0
        cycles: int = 0

        while ((best_sol.is_valid == False) and (retry_cnt < task.max_retry_attempts)) or (retry_cnt == 0):
            retry_cnt += 1
            curr_temp = task.init_temp
            cycles = retry_cnt*task.cycles

            while curr_temp > task.min_temp:
                for _ in range(task.cycles):
                    sol_cntr += 1

                    self.try_new_solution(task, best_sol, curr_sol, neighbour_sol, curr_temp)

                curr_temp *= task.cooling

        return best_sol, sol_cntr, retry_cnt

    def get_solution(self, task: TaskSAT) -> (SolutionSA, int, int):
        """
        Compute solution.
        
        Returns:
            tuple(SolutionSA, int, int) -- Tuple of (found_solution, number_of_solutions_visited, retry_count)
        """

        # np.random.seed(20191219)
        # random.seed(20191219)

        best_sol: SolutionSA = self.initial_solution(task)
        curr_sol: SolutionSA = self.initial_solution(task)
        neighbour_sol: SolutionSA = self.initial_solution(task)

        if task.evo_filepath is not None:
            return self.compute_solution_with_evo(task, best_sol, curr_sol, neighbour_sol)
        else:
            return self.compute_solution(task, best_sol, curr_sol, neighbour_sol)
 
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSAT = TaskSAT(context=context, parsed_data=parsed_data)
        
        solution, solution_cntr, retry_cnt = self.get_solution(task)

        # Pass solution
        out_vars: np.ndarray = np.zeros(task.num_of_vars + 1, dtype=int)
        for index, value in enumerate(solution.solution):
            if value == 1:
                out_vars[index] = index
            else:
                out_vars[index] = -index

        parsed_data.update({
            "found_value": solution.sum_weight,
            "vars_output": out_vars,
            "is_valid": solution.is_valid,
            "num_of_satisfied_clauses": solution.num_of_satisfied_clauses,
            "retry_count": retry_cnt,
            "elapsed_configs": solution_cntr
        })

        return parsed_data