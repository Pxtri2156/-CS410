import numpy as np
import random
import json 
import argparse
import os

# Problem size l: 10, 20, 40, 80, 160
# Tounament selection s = 4 
# Population size N 


class POPOP:
  def __init__(self,Population_size,Problem_size):
    self.Population_size = Population_size
    self.Problem_size = Problem_size
    self.Parents = None
    self.Pairs = None
    self.Childrens = None
    self.Tournament_Selection = []
    self.Number_evaluation = 0

  def Init_Population(self):
    self.Parents = np.random.randint(0,2,(self.Population_size,self.Problem_size))

  def Choose_Pair(self):
    '''
    Choose pair in parents to Create childrens
    Return:
      Pairs to create childrens
    '''
    self.Pairs = np.copy(self.Parents)
    np.random.shuffle(self.Pairs)
    #print("Pairs: \n ",self.Pairs)
  
  def Create_Children(self,Variation):
    """
    parameter:
      + Variation: is One-point crossover – 1X or  Uniform crossover - UX
    return:
      Childrens are created by Pairs
    """
    self.Childrens = np.copy(self.Pairs)
    for i in range(0,self.Population_size,2):

      #print("Pair: \n ",self.Childrens[i],"\n", self.Childrens[i+1])
      self.Crossover(Variation,self.Childrens[i], self.Childrens[i+1])
      #print("Pair after: \n ",self.Childrens[i],"\n", self.Childrens[i+1])
      

  def Crossover(self,Variation,Mother, Father):
    # One-point crossover – 1X)
    # Uniform crossover – UX

    if Variation == "1X":
      #Point_Crossover = random.randint(0,self.Problem_size-1)
      Point_Crossover = np.random.random_integers(self.Problem_size-1)
      #print("Point",Point_Crossover)
      for i in range(Point_Crossover + 1):
          temp = Mother[i]
          Mother[i] = Father[i]
          Father[i] = temp

    elif Variation == "UX":
      for i in range(self.Problem_size):
          prob_crossover = np.random.random_sample()
          #print("prob crossover: ", prob_crossover)
          if prob_crossover <= 0.5:
            temp = Mother[i]
            Mother[i] = Father[i]
            Father[i] = temp

  def Play_Tournament(self,fitness, s = 4):
    # Create Tounament 
   
    Tournament = np.concatenate((self.Pairs,self.Childrens))
    #print("Before shuffle Tournament: \n",Tournament)
    np.random.shuffle(Tournament)
    #print("After shuffle Tournament: \n",Tournament)
    Tournament_Selection = []
    if fitness == "One_Max":
      for i in range(0,self.Population_size*2,s):
        #print("Group {} : \n".format(i),Tournament[i:i+s])
        self.Number_evaluation += 1
        ind_winner = self.One_Max(Tournament[i:i+s])
        Tournament_Selection.append(Tournament[ind_winner + i])
    else:
      for i in range(0,self.Population_size*2,s):
        #print("Group {} : \n".format(i),Tournament[i:i+s])
        ind_winner = self.Trap(Tournament[i:i+s]) 
        self.Number_evaluation += 1
        Tournament_Selection.append(Tournament[ind_winner + i])

    self.Tournament_Selection = self.Tournament_Selection + Tournament_Selection
    #print("Tourament Selection: ",self.Tournament_Selection)

  def One_Max(self,group):
    '''
    + Argument: Group of individual 
    + Return: individual is the best with OneMax function 
    '''
    print("Using One_Max function")
    print("Info: Population_size-{} Problem_size-{}".format(self.Population_size,self.Problem_size))
    Winner = np.argmax(np.sum(group,axis = 1))
    #print(Winner)
    return Winner 

  def Trap(self,Group, k = 5 ):
    '''
    + Argument: Group of individual 
    + Return: individual is the best with Trap function 
    '''
    print("Using Trap function")
    print("Info: Population_size-{} Problem_size-{}".format(self.Population_size,self.Problem_size))
    result = []
    for i in range(Group.shape[0]):
      s = 0
      for j in range(0,len(Group[i]),k):
        Temp = np.sum(Group[i][j:j+k])
        if Temp <  4:
          Temp = 4 - Temp
        s = s + Temp
      result.append(s)
    Winner = np.argmax(result)
    #print(Winner)
    return Winner
        
  def Check_Convering(self):
    for i in range(1,self.Population_size):
      bool_array = self.Tournament_Selection[i] == self.Tournament_Selection[0]
      if bool_array.all() :
        continue
      else:
        return False
    return True


def Run_Popop(N,l,Crossover, Fitness):
  Is_Success = False  
  # STEP 0: Init population
  print("============= STEP 0: Init population =============")
  population = POPOP(N,l)
  population.Init_Population()

  # Evaluation
  iter = 0
  while 1:
    print("Parents: \n", population.Parents)
    
    # STEP 1: Choose Pairs
    print("============= STEP 1: Choose Pairs  =============")
    population.Choose_Pair()
    print("Pairs: \n",population.Pairs)

    # STEP 2: Crossover
    print("============= STEP 2: Crossover  =============")
    population.Create_Children(Crossover)
    print("Children: \n ", population.Childrens)

    # Selection s = 3 
    # STEP 3: Tounament
    #   STEP 3.1: Choose pair individual by random
    #   STEP 3.2: Use fitnees to choose best individual 
    print("============= STEP 3: Play Tournament  =============")
    for i in range(2):
      population.Play_Tournament(Fitness)
    population.Tournament_Selection = np.array(population.Tournament_Selection)
    print("Tournament Selection: \n",population.Tournament_Selection)
    
    Convergence = population.Check_Convering()
    print("Info: Population_size-{} Problem_size-{} Variant-{} Fitness-{} Convergence-{} Iter-{}".format(population.Population_size,population.Problem_size,Crossover,Fitness,Convergence, iter + 1))
    # Check Convering
    if Convergence :
      if np.all(1 == population.Tournament_Selection):
        Is_Success = True
      break
    
    population.Parents = np.copy(population.Tournament_Selection)
    population.Tournament_Selection = [] # Reset tourname selection
    iter +=1 

  print("Number Evaluation: ", population.Number_evaluation)
  dic_result = {"Is_Success": Is_Success,
                "Number_Evaluation":population.Number_evaluation
                }
  return dic_result


def Find_Upper_Bound(l,random_seeds,Crossover,Fitness):

  N_upper = 4
  while 1: 
    N_upper = N_upper*2
    print("[STATUS] Finding Upper Bound: Now, population size: {}".format(N_upper))
    dem = 0
    for random_seed in random_seeds:
      np.random.seed(random_seed)
      result = Run_Popop(N_upper,l,Crossover,Fitness)
      print("random seed: ", random_seed)
      if result["Is_Success"] == False:
        if N_upper < 8192:
          break 
        else:
          return -1 # -1 value is not find N_upper 
      else:
        dem += 1
    if dem == 10: # Success with 10 randomseed
      break 
  
  return N_upper

def Find_MRPS(l,N_upper,random_seeds,Crossover,Fitness):

  
  average_number_of_evaluations = None
  if N_upper != -1:
    N_lower = N_upper / 2
    
    while (N_upper - N_lower)/N_upper > 0.1:
      N = (N_upper - N_lower) / 2 
      average_number_of_evaluations = []
      dem = 0
      for random_seed in random_seeds:
        np.random.seed(random_seed)
        result = Run_Popop(N_upper,l,Crossover,Fitness)
        print("random seed: ", random_seed)
        if result["Is_Success"] == False:
          break
        else:
          average_number_of_evaluations.append(result["Number_Evaluation"])
          dem += 1
      if dem == 10: # Success with 10 randomseed
        N_upper = N
      else: 
        N_lower = N
      
      if N_upper - N_lower <= 2:
        break
    average_number_of_evaluations = np.sum(average_number_of_evaluations,axis = 0) / 10
  return N_upper, average_number_of_evaluations

def Run_Bisection(l,random_seeds,Crossover,Fitness):
  N_upper = Find_Upper_Bound(l,random_seeds,Crossover, Fitness)
  print("N_upper: ", N_upper)
  MRPS, average_number_of_evaluations = Find_MRPS(l,N_upper,random_seeds,Crossover,Fitness)
  print("MRPS: {} \nAverage_number_of_evaluations: {} ".format(MRPS, average_number_of_evaluations))
  return MRPS, average_number_of_evaluations
def main(args):
  
  # ===== Test =====#
  Problem_size_lst = [10, 20, 40, 80, 160] # Problem size
  
  
  Crossover = args['Crossover']
  Fitness = args['Fitness']

  # Init random_seeds array 
  
  MSSV = 18521530
  random_seeds = []
  s = 0
  for i in range(10):
    row = []
    for j in range(10):
      row.append(s + MSSV)
      s += 1
    random_seeds.append(row)
  
  result_final = {}
  stop = False
  for l in Problem_size_lst :
  # random_seeds = [[0,1,2,3,4,5,6,7,8,9]]
    dic_result = {"MRPS": [],
                  "Avg_eval": []
                  }
    # Run 
    for i in range(len(random_seeds)):
      
      MRPS, average_number_of_evaluations = Run_Bisection(l,random_seeds[i],Crossover,Fitness)
      dic_result["MRPS"].append(MRPS)
      dic_result["Avg_eval"].append(average_number_of_evaluations )

      if MRPS == -1:
        stop = True
        break
    
    print("Experience result: ",dic_result)
    result_final[l] = dic_result

    if stop :
      break
 

  #Run_Bisection(N,l) # Run 10 iterate
  # Save result 
  file_name = "Experience_" + args["Crossover"] + "_" + args['Fitness'] + ".json"
  path = args["path_save"]
  file = open(file_name,"w")
  json.dump(result_final,file)
  file.close()
  print("Good")
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='POPOP')
  parser.add_argument('-p','--path_save', type=str, required=True, help='The path of image need process')
  parser.add_argument('-c','--Crossover', type=str, required=True, help='Function Crossover: 1X or UX')
  parser.add_argument('-f','--Fitness', type=str, required=True, help='Function Fitness: One_Max or Trap')
  main(vars(parser.parse_args()))