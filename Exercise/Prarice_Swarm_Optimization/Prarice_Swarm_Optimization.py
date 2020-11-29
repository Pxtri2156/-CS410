import numpy as np
import argparse
import os
import json
import sys
sys.path.append('./')

from config import NEIHBORHOOD_TOPOLOGY, ACCELERATION, MSSV, \
                    INERTIA_W, GENERATION_MAX, PROBLEM, THRESOLD



class Pso:

    def __init__(self,population_size, problem_size):
        self.neighborhood_topology = None # 1 is Ring or 2 is Star
        self.population_size = population_size
        self.problem_size = problem_size
        self.acceleration = ACCELERATION
        self.vector_random = np.random.rand(1,2)
        self.inertia_w = INERTIA_W 
        self.generation_max = GENERATION_MAX
        self.type_function = "Rastrigin" # Default type function Rastrigin
        self.population = None
        self.problem = None
        self.social = None
        self.n_eval = 0

        self.log = {
            'log_population': [],
            'best_solution': None,
            'val_best_solution':None,
            'dis_true_global':None,
            'randomseed': None

        }
        
    
    def init_population(self,type_function):
        self.type_function = type_function
        self.problem = PROBLEM[type_function]
        self.population = np.random.uniform(self.problem['lower'], self.problem['upper'], \
            size = (self.population_size, self.problem_size))

    def find_social(self,type_neighborhood ):
        self.neighborhood_topology = type_neighborhood
        best_neighbors = []
        if self.neighborhood_topology == 1: # Neighborhood topology ring
            for i in range(self.population_size):
                left = i -1 
                if i + 1 == self.population_size:
                    right = 0
                else:
                    right = i + 1
                
                # print("Current: ", self.population[i], np.apply_along_axis(self.problem['formula'],1,[self.population[i]]))
                # print("Left: ", self.population[left], np.apply_along_axis(self.problem['formula'],1,[self.population[left]]))
                # print("Right: ", self.population[right], np.apply_along_axis(self.problem['formula'],1,[self.population[right]]))
                # find best element in 3 element
                best_neighbor = self.population[left]
                if np.apply_along_axis(self.problem['formula'],1,[self.population[i]]) \
                    < np.apply_along_axis(self.problem['formula'],1,[best_neighbor]):
                    best_neighbor = self.population[i]
                if np.apply_along_axis(self.problem['formula'],1,[self.population[right]]) \
                    < np.apply_along_axis(self.problem['formula'],1,[best_neighbor]):
                    best_neighbor = self.population[right]
                # print("best neighbor: ",best_neighbor)
                best_neighbors.append(best_neighbor)

            self.n_eval += 3*self.population_size # update number evaluation
            best_neighbors = np.array(best_neighbors)

        elif self.neighborhood_topology == 2:  # Neighborhood topology star
            best_neighbor =  self.population[0]                          
            for i in range(1,self.population_size):
                # print("Current: ", self.population[i], np.apply_along_axis(self.problem['formula'],1,[self.population[i]]))
                if np.apply_along_axis(self.problem['formula'],1,[self.population[i]]) \
                    < np.apply_along_axis(self.problem['formula'],1,[best_neighbor]):
                    best_neighbor = self.population[i]
                # print("best neighbor: ",best_neighbor)
            best_neighbors = np.full((self.population_size, self.problem_size), best_neighbor)
            self.n_eval += 2*self.population_size # update number evaluation
        else:
            print("Please choose type neighborhood topology !!!")

        return best_neighbors
    
    def find_cognitive(self,cr_cognitive):
        for i in range(self.population_size):
            # print('population {} {} {}'.format(i, self.population[i], \
            #     np.apply_along_axis(self.problem['formula'],1,[self.population[i]])))
            # print('cognitive {} {} {} '.format(i, cr_cognitive[i], \
            #     np.apply_along_axis(self.problem['formula'],1,[cr_cognitive[i]])))
            if  np.apply_along_axis(self.problem['formula'],1,[self.population[i]]) \
                <  np.apply_along_axis(self.problem['formula'],1,[cr_cognitive[i]]):
                cr_cognitive[i] = np.copy(self.population[i])
        self.n_eval += 2*self.population_size

    def run(self, type_function, type_neighborhood):
        # Use this function when population exits
        name_topology = None
        if type_neighborhood == 1:
            name_topology  = "ring"
        else:
            name_topology = "star"
        prev_velocity = np.zeros((self.population_size, self.problem_size)) 
        # Generation 0:
        ## Find cognitive
        cognitive = np.copy(self.population)
        # print('cognitive: ', cognitive)
        ## Best social
        social = self.find_social(type_neighborhood)
        ## Compute velocity
        self.vector_random = np.random.rand(1, 2)

        velocity = self.inertia_w*prev_velocity \
            + self.acceleration[0]*self.vector_random[0,0]*(cognitive - self.population) \
            + self.acceleration[1]*self.vector_random[0,1]*(social - self.population) 
        # print('Velocity ', velocity) 
        # print("velocity ",velocity)
        ## Generate new position
        self.population = self.population + velocity
        print("[INFO] prob_n: {}, prop_s: {}, prob_s: {},topology: {}, gen: 0".format(\
            type_function, self.population_size, self.problem_size, name_topology))

        # Save log
        self.log["log_population"].append(self.population.tolist())
       
        # print("Current population", self.population)

        # print("Object value: ", np.apply_along_axis(self.problem['formula'],1,self.population))
        # Check range of position: 
        self.check_range()
        # Residual generation: 
        if self.problem_size == 2: 
            for i in range(1,self.generation_max+1):
                print("[INFO] prob_n: {}, prop_s: {}, prob_s: {},topology: {}, gen: {} n_eval: {} ".format(\
                    type_function, self.population_size, self.problem_size, name_topology,i, self.n_eval))\
                # print("Current population", self.population)
                # print("Object value: ", np.apply_along_axis(self.problem['formula'],1,self.population))
                ## Update pre_velocity
                prev_velocity = velocity 
                ## Find cognitive
                self.find_cognitive(cognitive)
                # print('cognitive: ', cognitive)
                # print('population: ', self.population)
                ## Find best social
                social = self.find_social(type_neighborhood)

                ## Compute veloctiy
                self.vector_random = np.random.rand(1, 2)
                
                velocity = self.inertia_w*prev_velocity \
                + self.acceleration[0]*self.vector_random[0,0]*(cognitive - self.population) \
                + self.acceleration[1]*self.vector_random[0,1]*(social - self.population) 
                ## Infer new population
                self.population = self.population + velocity

                ## Save log:
                self.log["log_population"].append(self.population.tolist())
               

                ## Check range 
                self.check_range()

        else:     # problem size = 10
            i = 1
            while self.n_eval <= 1e+6:
                print("[INFO] prob_n: {}, prop_s: {}, prob_s: {},topology: {}, gen: {} n_eval: {} ".format(\
                    type_function, self.population_size, self.problem_size, name_topology,i, self.n_eval))\
                
                # print("Current population \n", self.population)

                # print("Object value: \n", np.apply_along_axis(self.problem['formula'],1,self.population))
                
                ## Update pre_velocity
                prev_velocity = velocity 
                ## Find cognitive
                self.find_cognitive(cognitive)
                # print('cognitive: ', cognitive)
                # print('population: ', self.population)
                ## Find best social
                social = self.find_social(type_neighborhood)

                ## Compute veloctiy
                self.vector_random = np.random.rand(1, 2)
                # print('random ', self.vector_random)

                velocity = self.inertia_w*prev_velocity \
                + self.acceleration[0]*self.vector_random[0,0]*(cognitive - self.population) \
                + self.acceleration[1]*self.vector_random[0,1]*(social - self.population)

                # print('Velocity \n', velocity) 
                ## Infer new population
                self.population = self.population + velocity
                ## Wrtie log
                self.log["log_population"].append(self.population.tolist())
                # input("Fix bug")
                ## Check range
                
                self.check_range()
                if self.check_conveger():
                    
                    break
                i += 1  
        best_solution,  value_object = self.find_best_solution(type_neighborhood, cognitive)
        self.log["best_solution"] = best_solution.tolist()
        self.log["val_best_solution"] = float(value_object)
        self.log["dis_true_global"] = float(np.abs(value_object - self.problem["optimal_val"]))

    def write_log(self):

        pass
    
    def check_conveger(self):
        # print("check conveger ", np.abs(np.apply_along_axis(self.problem['formula'],1,self.population) \
        #     - self.problem['optimal_val']) )
        
        bool_array = np.abs(np.apply_along_axis(self.problem['formula'],1,self.population) \
            - self.problem['optimal_val']) < THRESOLD
        
        # print('bool_array: ', bool_array)
        
        if np.sum(bool_array)/len(bool_array) >= 0.95:
            return True
        else:
            return False
        
    def check_range(self): 
        self.population[self.population >= self.problem['upper']] = self.problem['upper']
        self.population[self.population <= self.problem['lower']] = self.problem['lower']

    def find_best_solution(self, type_neighborhood, population ):
        best_solution = None
        if type_neighborhood == 2:
            best_solution = population[0]
        else:
            index_best_solution = np.argmin(np.abs(np.apply_along_axis(self.problem['formula'],1,population) - self.problem['optimal_val']))
            best_solution = np.copy(population[index_best_solution])
        
        
        return best_solution, self.problem['formula'](best_solution)
    
        
    
def main(args):
    # Init random seed
    if args["probsize"] == 2:
        N = 1
        randseeds = np.array([MSSV])
    else:
        N = 10
        randseeds = np.full((10,),MSSV) + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Create file name
    if args['topology'] == 1:
        name_topology  = "ring"
    else:
        name_topology = "star"
    file_name = args['problem'] + '_' + name_topology+  '_' + str(args['popsize']) + '_' + str(args['probsize']) + '.json'
    path_log = os.path.join('./Experimental_result',file_name)
    log_file = open(path_log, "w")
    result_population = []
    for i in range(N):
        np.random.seed(randseeds[i])
        p = Pso(args["popsize"], args["probsize"])
        p.init_population(args["problem"]) # Initial with problem
        print("Origin population", p.population)

        print("Object value: ", np.apply_along_axis(p.problem['formula'],1,p.population))
        

        p.run(args["problem"], args["topology"])
        print("[INFO] prob_n: {}, prop_s: {}, prob_s: {},topology: {}".format(\
            args["problem"], args["popsize"], args["probsize"], args["topology"]))
        
        print("Result: ", p.population)
        print("Object value: ", np.apply_along_axis(p.problem['formula'], 1, p.population))
        print("[INFO] prob_n: {}, prop_s: {}, prob_s: {},topology: {} state: DONE".format(\
                    args["problem"], p.population_size, p.problem_size, name_topology))\
          
        
        ## Wrtie randomseed
        p.log['randomseed'] = randseeds[i].tolist()
        result_population.append(p.log)
    
    json.dump(result_population,log_file)
    # Save log file
    log_file.close()
    

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Config to run PSO')
    parser.add_argument('--topology', '-t', required=True, 
                        type=int, help='ring: 1 or star: 2')
    parser.add_argument('--problem', '-p', required=True, 
                        type=str, help='Name of problem')
    parser.add_argument('--popsize', '-s1', default = 32, 
                        type=int, help='Size of population ')
    parser.add_argument('--probsize', '-s2', default = 2, 
                        type=int, help='Size of population ')
    
    args = vars(parser.parse_args())
    main(args)
